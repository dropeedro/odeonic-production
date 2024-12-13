from fastapi import APIRouter, Request, HTTPException
import stripe
from app.services.user_service import update_subscription

router = APIRouter()
stripe.api_key = "sk_test_51N6fflGY6BYBTtJUSwOPFIwn3Ln3x07LompvRhNCQSjD5gjnh17rKe7VMJ5VWL08iKQQocXbozNE0AkW57xOmQM700S1Twcn3K"

# @router.post("/webhook")
# async def stripe_webhook(request: Request):
#     payload = await request.body()
#     sig_header = request.headers.get("Stripe-Signature")
#     webhook_secret = "whsec_106eb91daef19266bb3a98f6ddfb4d3927d2cb6ea20bfd7ec088c0e01a3e9034"

#     try:
#         # Construcción del evento Stripe
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, webhook_secret
#         )
#         print(f"Webhook received: {event['type']}")

#         if event["type"] == "checkout.session.completed":
#             session = event["data"]["object"]
#             customer_email = session.get("customer_email")
#             subscription_id = session.get("subscription")

#             if not subscription_id:
#                 print(f"Subscription ID is missing in the session: {session}")
#                 raise HTTPException(status_code=400, detail="Subscription ID is missing in the session.")

#             # Recuperar información de la suscripción desde Stripe
#             try:
#                 subscription = stripe.Subscription.retrieve(subscription_id)
#             except Exception as e:
#                 print(f"Error retrieving subscription from Stripe: {str(e)}")
#                 raise HTTPException(status_code=500, detail=f"Error retrieving subscription: {str(e)}")

#             plan_id = subscription["items"]["data"][0]["price"]["id"]
#             status = subscription["status"]
#             start_date = subscription["current_period_start"]
#             end_date = subscription["current_period_end"]

#             # Datos para actualizar en MongoDB
#             subscription_data = {
#                 "subscription_id": subscription_id,
#                 "status": status,
#                 "plan": plan_id,
#                 "start_date": start_date,
#                 "end_date": end_date,
#             }

#             # Actualizar los datos del usuario en MongoDB
#             update_subscription(customer_email, subscription_data)

#             print(f"Updated subscription for user: {customer_email}")
#     except ValueError as e:
#         print("Invalid payload:", str(e))
#         raise HTTPException(status_code=400, detail="Invalid payload")
#     except stripe.error.SignatureVerificationError as e:
#         print("Invalid signature:", str(e))
#         raise HTTPException(status_code=400, detail="Invalid signature")
#     except Exception as e:
#         print("Unhandled exception:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))

#     return {"status": "success"}

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = "whsec_106eb91daef19266bb3a98f6ddfb4d3927d2cb6ea20bfd7ec088c0e01a3e9034"

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        print(f"Webhook received: {event['type']}")

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            customer_email = session.get("customer_details", {}).get("email")
            subscription_id = session.get("subscription")

            if not customer_email:
                print("Customer email not found in session:", session)
                return {"status": "ignored"}

            if not subscription_id:
                print("Subscription ID is missing in the session:", session)
                return {"status": "ignored"}

            # Obtén la suscripción de Stripe para más detalles
            subscription = stripe.Subscription.retrieve(subscription_id)
            plan_id = subscription["items"]["data"][0]["price"]["id"]
            status = subscription["status"]
            start_date = subscription["current_period_start"]
            end_date = subscription["current_period_end"]

            # Datos para actualizar MongoDB
            subscription_data = {
                "subscription_id": subscription_id,
                "status": status,
                "plan": plan_id,
                "start_date": start_date,
                "end_date": end_date,
            }

            # Actualizar MongoDB
            update_subscription(customer_email, subscription_data)
            print(f"Updated subscription for user: {customer_email}")

    except Exception as e:
        print("Webhook processing error:", str(e))
        raise HTTPException(status_code=400, detail="Webhook error")
