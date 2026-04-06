from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    content: str
    user_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    id: str
    reply: str
    status: str = "success"
