from app.db.mongo import db

def create_plan(plan_data):
    result = db.plans.insert_one(plan_data)
    return str(result.inserted_id)

def get_plan_by_id(plan_id):
    return db.plans.find_one({"_id": plan_id})
