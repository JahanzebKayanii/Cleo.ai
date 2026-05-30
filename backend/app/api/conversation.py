from fastapi import APIRouter
from pydantic import BaseModel

from app.services.conversation_service import clear_session, get_response

router = APIRouter(prefix="/conversation", tags=["conversation"])


class MessageRequest(BaseModel):
    session_id: str
    message: str
    phone: str = ""


class MessageResponse(BaseModel):
    session_id: str
    response: str


@router.post("/message", response_model=MessageResponse)
async def message(body: MessageRequest):
    reply = await get_response(body.session_id, body.message, caller_phone=body.phone)
    return MessageResponse(session_id=body.session_id, response=reply)


@router.post("/end")
async def end_session(session_id: str):
    clear_session(session_id)
    return {"status": "session cleared", "session_id": session_id}
