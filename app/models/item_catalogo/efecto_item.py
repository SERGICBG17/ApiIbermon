from pydantic import BaseModel
from typing import Any, Optional

class EfectoItem(BaseModel):
    tipo_efecto: str                  # "curacion", "captura", "subida_stat", etc
    valor: Optional[Any] = None       # cantidad curada, bonus de captura, etc