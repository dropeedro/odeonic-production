from bson import ObjectId  
from app.models.plan import Plan
from app.db.mongo import db

class PlanService:
    @staticmethod
    def get_all_plans():
        return list(db["plans"].find({}))

    @staticmethod
    def create_plan(plan: Plan):
        db["plans"].insert_one(plan.dict())
        return plan

    @staticmethod
    def update_plan(plan_id: str, plan: Plan):
        # Convertir el plan_id a ObjectId
        object_id = ObjectId(plan_id)
        # Actualizar solo los campos no nulos
        update_data = {k: v for k, v in plan.dict().items() if v is not None}

        result = db["plans"].update_one({"_id": object_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Plan not found")
        return plan

    @staticmethod
    def delete_plan(plan_id: str):
        object_id = ObjectId(plan_id)  # Convertir el plan_id a ObjectId
        result = db["plans"].delete_one({"_id": object_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Plan not found")
        return {"message": "Plan deleted successfully"}
