from fastapi import APIRouter
from schema import ContactMessage
from services.email_feedback import send_email

router = APIRouter()


@router.post("")
async def contact(data: ContactMessage):

    await send_email(
        data.name,
        data.email,
        data.message
    )

    return {"message": "Sent"}