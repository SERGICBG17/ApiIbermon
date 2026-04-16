from pydantic import BaseModel, Field


class MensajeChatbotSchema(BaseModel):
    mensaje: str = Field(..., min_length=1, max_length=500)


class RespuestaChatbotSchema(BaseModel):
    respuesta: str
