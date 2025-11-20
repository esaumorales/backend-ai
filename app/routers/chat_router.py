# app/routers/chat_router.py
from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import generate_chat_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    reply = await generate_chat_response(payload.message)
    return ChatResponse(response=reply)
