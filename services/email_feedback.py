import resend
from config import settings


resend.api_key = settings.resend_api_key.get_secret_value()

async def send_email(name: str, email: str, message: str):

    resend.Emails.send({
        "from": "Portfolio <onboarding@resend.dev>",
        "to": settings.email_user,
        "subject": f"New message from {name}",
        "html": f"""
        <h2>New Portfolio Contact Message</h2>

        <p><strong>Name:</strong> {name}</p>

        <p><strong>Email:</strong> {email}</p>

        <p><strong>Message:</strong></p>

        <p>{message}</p>
        """
    })
