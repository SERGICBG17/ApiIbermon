from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
from bson import ObjectId


# --- REQUEST ---

class UsuarioRegistroSchema(BaseModel):
    """Datos necesarios para registrar un nuevo usuario."""
    username: str
    email: EmailStr
    password: str


class UsuarioLoginSchema(BaseModel):
    """Datos necesarios para hacer login."""
    username: str
    password: str


# --- RESPONSE ---

class UsuarioPublicoSchema(BaseModel):
    """Datos del usuario que se devuelven al cliente. Sin password."""
    id: str
    username: str
    email: EmailStr
    fecha_registro: datetime
    partidas: List[str] = []

    class Config:
        populate_by_name = True


class TokenSchema(BaseModel):
    """Token JWT que se devuelve tras el login."""
    access_token: str
    token_type: str = "bearer"
