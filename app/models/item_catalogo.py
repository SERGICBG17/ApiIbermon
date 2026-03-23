from beanie import Document
from pydantic import BaseModel
from typing import Any, Optional

class EfectoItem(BaseModel):
    tipo_efecto: str                  # "curacion", "captura", "subida_stat", etc
    valor: Optional[Any] = None       # cantidad curada, bonus de captura, etc


class ItemCatalogo(Document):
    numero: int                       # PK
    nombre: str
    descripcion: str
    tipo: str                         # "curacion", "captura", "batalla", "clave"
    efecto: EfectoItem
    precio: int

    class Settings:
        name = "item_catalogo"
