from datetime import datetime
from app.database import db

def update_subscription(user_email: str, subscription_data: dict):
    """
    Updates the subscription status of a user in the database.

    Args:
        user_email (str): Email of the user to update.
        subscription_data (dict): Subscription data obtained from Stripe.
    """
    user = db.users.find_one({"email": user_email})
    if not user:
        raise ValueError(f"No user found with email {user_email}")

    # Calculate subscription duration in days
    start_date = datetime.fromtimestamp(subscription_data["start_date"])
    end_date = datetime.fromtimestamp(subscription_data["end_date"])
    duration = (end_date - start_date).days

    # Update the user in the database
    db.users.update_one(
        {"email": user_email},
        {
            "$set": {
                "subscription_id": subscription_data["subscription_id"],
                "subscription_status": subscription_data["status"],
                "subscription_plan": subscription_data["plan"],
                "subscription_start_date": start_date.isoformat(),
                "subscription_end_date": end_date.isoformat(),
                "subscription_duration": duration,
            }
        },
    )

    return {"message": f"Subscription updated for user {user_email}"}

def get_subscription_status(user_email: str):
    """
    Retrieves the subscription status of a user.

    Args:
        user_email (str): Email of the user.

    Returns:
        dict: Subscription status details or an error message.
    """
    user = db.users.find_one({"email": user_email})
    if not user:
        raise ValueError(f"No user found with email {user_email}")

    subscription_data = {
        "subscription_id": user.get("subscription_id"),
        "subscription_status": user.get("subscription_status"),
        "subscription_plan": user.get("subscription_plan"),
        "subscription_start_date": user.get("subscription_start_date"),
        "subscription_end_date": user.get("subscription_end_date"),
        "subscription_duration": user.get("subscription_duration"),
    }

    return subscription_data

def create_user(email: str, password: str = None, oauth_provider: str = None, oauth_id: str = None):
    """
    Creates a new user in the database.

    Args:
        email (str): User's email.
        password (str): User's password (optional, for non-OAuth users).
        oauth_provider (str): OAuth provider name (optional).
        oauth_id (str): OAuth ID (optional).

    Returns:
        dict: Details of the newly created user.
    """
    user = db.users.find_one({"email": email})
    if user:
        raise ValueError(f"User with email {email} already exists")

    user_data = {
        "email": email,
        "password": password,  # This should be hashed in a real implementation
        "oauth_provider": oauth_provider,
        "oauth_id": oauth_id,
        "roles": ["user"],
        "subscription_id": None,
        "subscription_status": "inactive",
        "subscription_plan": None,
        "subscription_start_date": None,
        "subscription_end_date": None,
        "subscription_duration": 0,
    }

    result = db.users.insert_one(user_data)
    return {"id": str(result.inserted_id), "email": email}
