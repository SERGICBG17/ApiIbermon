from beanie import Document
from pydantic import EmailStr
from datetime import datetime
from typing import List
from bson import ObjectId

class Usuario(Document):
    username: str
    email: EmailStr
    hashed_password: str
    fecha_registro: datetime = datetime.utcnow()
    partidas: List[ObjectId] = []

    class Settings:
        name = "usuarios"
