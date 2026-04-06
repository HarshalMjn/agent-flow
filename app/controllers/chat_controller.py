from app import services
from app.schemas.chat_schemas import ChatMessage, ChatResponse
from app.services.chat_service import chat_service

class ChatController:
    async def handle_chat_trigger(self, message: ChatMessage) -> ChatResponse:
        # Business logic for chat handled via service
        return await chat_service.process_message(message)

chat_controller = ChatController()
