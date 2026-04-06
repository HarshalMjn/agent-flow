from app.schemas.chat_schemas import ChatMessage, ChatResponse
import uuid

class ChatService:
    async def process_message(self, message: ChatMessage) -> ChatResponse:
        # Simple echo for now, can be expanded to LLM call later
        return ChatResponse(
            id=str(uuid.uuid4()),
            reply=f"Echo: {message.content}",
            status="success"
        )

chat_service = ChatService()
