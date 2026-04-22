from typing import Optional, Any

from pydantic import BaseModel

class EfectoItemSchema(BaseModel):
    tipo_efecto: str
    valor: Optional[Any] = None