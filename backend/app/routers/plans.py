from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.models.plan import Plan
from app.services.plan_service import PlanService
from app.services.user_service import update_subscription
import stripe
import os
from app.db.mongo import db

# Router initialization
router = APIRouter()

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_API_KEY")  # Load your Stripe API key from environment variables
stripe.log = "debug"

# Price mapping
price_mapping = {
    "personal": "price_1QN3weGY6BYBTtJUr4Zj1sxZ",  # Price ID for Personal plan
    "business": "price_1QN2KIGY6BYBTtJULpFghusG",   # Price ID for Business plan
}

# Models
class SubscriptionRequest(BaseModel):
    plan_id: str
    email: EmailStr

class SubscriptionUpdateRequest(BaseModel):
    user_email: str
    subscription_data: dict

@router.get("/", response_model=list[Plan])
async def get_all_plans():
    """
    Retrieve all available plans from the database.
    """
    plans = db["plans"].find({})
    return [
        {
            "id": str(plan["_id"]),  # Solo si necesitas incluir el `_id` como referencia adicional
            **plan
        }
        for plan in plans
    ]

@router.post("/", response_model=Plan)
async def create_plan(plan: Plan):
    """
    Create a new plan in the database.
    """
    return PlanService.create_plan(plan)

from bson import ObjectId

@router.put("/{plan_type}", response_model=Plan)
async def update_plan(plan_type: str, plan: Plan):
    # Depuración: imprime los datos recibidos
    print(f"Received Plan Type: {plan_type}")
    print(f"Received Plan Data: {plan.dict(exclude_unset=True)}")  # Excluye campos no establecidos

    if not plan_type:
        raise HTTPException(status_code=400, detail="Invalid plan type")

    existing_plan = db.plans.find_one({"type": plan_type})
    if not existing_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Actualización de datos, excluyendo campos innecesarios
    update_data = plan.dict(exclude={"id"}, exclude_unset=True)  # Excluir 'id' del payload
    result = db.plans.update_one(
        {"type": plan_type},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Failed to update plan")

    updated_plan = db.plans.find_one({"type": plan_type})
    updated_plan["_id"] = str(updated_plan["_id"])  # Convertir ObjectId a string
    return updated_plan



@router.delete("/{plan_type}")
async def delete_plan(plan_type: str):
    """
    Delete a plan from the database by its type.
    """
    # Verificar si el tipo de plan está definido
    if not plan_type:
        raise HTTPException(status_code=400, detail="Invalid plan type")

    # Intentar encontrar y eliminar el plan por 'type'
    result = db.plans.delete_one({"type": plan_type})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")

    return {"message": f"Plan with type '{plan_type}' deleted successfully"}



# Endpoint to create a subscription session
@router.post("/create-subscription-session")
async def create_subscription_session(request: SubscriptionRequest):
    """
    Create a Stripe Checkout session for a subscription.
    """
    print(f"Received data: {request.dict()}")
    price_id = price_mapping.get(request.plan_id)

    if not price_id:
        raise HTTPException(status_code=400, detail="Invalid plan ID")

    try:
        # Create a customer or use the provided email
        customer = stripe.Customer.create(email=request.email)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {"price": price_id, "quantity": 1},
            ],
            customer=customer.id,  # Associate the session with the customer
            # success_url=f"http://localhost:5173/dashboard?success=true&email={request.email}&plan={request.plan_id}",
            success_url=f"http://localhost:5173/user?success=true&email={request.email}&plan={request.plan_id}",
            cancel_url="http://localhost:5173/dashboard?canceled=true",
        )
        print(f"Session successfully created: {session.url}")
        return {"url": session.url}
    except stripe.error.StripeError as e:
        print(f"Error in Stripe: {e}")
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")

# Endpoint to validate a price
@router.post("/validate-price")
async def validate_price(price_id: str):
    """
    Validate if a price exists in Stripe.
    """
    try:
        price = stripe.Price.retrieve(price_id)
        return {"valid": True, "price": price}
    except stripe.error.InvalidRequestError as e:
        return {"valid": False, "error": str(e)}


@router.post("/update-subscription")
async def test_update_subscription(request: SubscriptionUpdateRequest):
    """
    Update subscription data for a user in MongoDB.
    """
    try:
        print(f"Received update request: {request.dict()}")  # Log para depuración
        result = update_subscription(request.user_email, request.subscription_data)
        print(f"Update result: {result}")  # Log para depuración
        return result
    except ValueError as e:
        print(f"Error updating subscription: {str(e)}")  # Log para depuración
        raise HTTPException(status_code=404, detail=str(e))
