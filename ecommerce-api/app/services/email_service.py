


import resend
import os
from typing import Dict
from dotenv import load_dotenv
from app.config import settings

load_dotenv()

resend.api_key = settings.RESEND_API_KEY

def send_welcome_email(email: str, code: str) -> Dict:
    params = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["bodyafrozen890@gmail.com"],
        "subject": "Welcome to E-commerce API",
        "html": f"<p> Your verify code!: <strong>{code}</strong></p>",
    }
    return resend.Emails.send(params)

def send_reset_email(email: str, code: str) -> Dict:
    params = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["bodyafrozen890@gmail.com"],
        "subject": "Password reset",
        "html": f"<p> Your reset code: <strong>{code}</strong></p>"
    }
    return resend.Emails.send(params)

def send_order_status_email(email: str, order_id: int, status: str) -> Dict:
    params = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["bodyafrozen890@gmail.com"],
        "subject": f"Order #{order_id} status updated",
        "html": f"<p>Your order <strong>#{order_id}</strong> status changed to <strong>{status}</strong></p>"
    }
    return resend.Emails.send(params)