import asyncio
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.config.settings import settings
from app.routes import workflows, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Temporal client, DB, etc.
    print(f"Starting {settings.APP_NAME}...")
    yield
    # Shutdown
    print(f"Stopping {settings.APP_NAME}...")

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["Workflows"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/v1/events")
async def events(request: Request):
    """
    SSE endpoint for real-time workflow status updates.
    """
    async def event_generator():
        while True:
            # Check for client disconnect
            if await request.is_disconnected():
                break
            
            # This is a dummy event, in real app we'd pull from Redis or a queue
            data = {"type": "heartbeat", "content": "keeping alive"}
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
