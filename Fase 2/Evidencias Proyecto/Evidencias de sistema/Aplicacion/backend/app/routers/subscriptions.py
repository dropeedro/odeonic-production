from fastapi import APIRouter, Depends, HTTPException
import stripe

router = APIRouter()

stripe.api_key = "sk_test_your_stripe_secret_key"

@router.get("/subscription-status")
async def get_subscription_status(email: str):
    # Consulta la base de datos para verificar el estado de la suscripción
    user = db.users.find_one({"email": email})
    if not user or not user.get("subscription_id"):
        raise HTTPException(status_code=404, detail="No active subscription found")

    # Verifica el estado de la suscripción en Stripe
    try:
        subscription = stripe.Subscription.retrieve(user["subscription_id"])
        return {"status": subscription["status"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
