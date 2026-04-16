from fastapi import APIRouter

from app.schemas.chatbot_schema import MensajeChatbotSchema, RespuestaChatbotSchema
from app.services import chatbot_service

router = APIRouter(prefix="/chatbot", tags=["Chatbot IberBot"])


@router.post("/mensaje", response_model=RespuestaChatbotSchema)
async def enviar_mensaje(body: MensajeChatbotSchema):
    """Envía un mensaje a IberBot y devuelve su respuesta."""
    respuesta = await chatbot_service.responder(body.mensaje)
    return RespuestaChatbotSchema(respuesta=respuesta)
