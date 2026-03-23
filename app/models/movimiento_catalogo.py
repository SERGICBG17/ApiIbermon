from beanie import Document
from typing import Optional

class MovimientoCatalogo(Document):
    numero: int                       # PK
    nombre: str
    tipo: str
    potencia: int
    precision: int
    pp: int                           # usos del movimiento
    descripcion: str
    efecto: Optional[str] = None      # descripcion del efecto especial si lo tiene

    class Settings:
        name = "movimiento_catalogo"
