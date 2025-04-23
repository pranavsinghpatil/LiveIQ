import requests
import os

def register_user_admin_api(email: str, password: str, username: str):
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project-id.supabase.co")
    SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "your-service-role-token")

    headers = {
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "apikey": SERVICE_ROLE_KEY,  # REQUIRED for Supabase Admin API
        "Content-Type": "application/json"
    }

    payload = {
        "email": email,
        "password": password,
        "user_metadata": {
            "username": username
        },
        "email_confirm": True   # Remove in production -----------------------------------
    }

    response = requests.post(
        f"{SUPABASE_URL}/auth/v1/admin/users",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
