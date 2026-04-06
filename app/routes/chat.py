from fastapi import APIRouter
from app.controllers import chat_controller
from app.schemas import chat_schemas

router = APIRouter()

@router.post("/", response_model=chat_schemas.ChatResponse)
async def chat_trigger(message: chat_schemas.ChatMessage):
    return await chat_controller.handle_chat_trigger(message)
