from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.business_service import get_business
from app.services.conversation_service import clear_session, get_response
from app.services.customer_service import get_caller_context

router = APIRouter(prefix="/conversation", tags=["conversation"])


class MessageRequest(BaseModel):
    session_id: str
    message: str
    phone: str = ""
    business_id: int = 1


class MessageResponse(BaseModel):
    session_id: str
    response: str


@router.post("/message", response_model=MessageResponse)
async def message(body: MessageRequest, db: AsyncSession = Depends(get_db)):
    caller_info = await get_caller_context(db, body.phone) if body.phone else {}
    config = await get_business(db, body.business_id)
    reply = await get_response(body.session_id, body.message, caller_phone=body.phone, caller_info=caller_info, config=config)
    return MessageResponse(session_id=body.session_id, response=reply)


@router.post("/end")
async def end_session(session_id: str):
    clear_session(session_id)
    return {"status": "session cleared", "session_id": session_id}
