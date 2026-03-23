from beanie import Document, PydanticObjectId
from pydantic import EmailStr
from datetime import datetime
from typing import List


class Usuario(Document):
    username: str
    email: EmailStr
    hashed_password: str
    fecha_registro: datetime = datetime.utcnow()
    partidas: List[PydanticObjectId] = []

    class Settings:
        name = "usuarios"
