from beanie import Document
from typing import Optional

class MovimientoCatalogo(Document):
    numero: int                            # PK
    nombre: str
    tipo: str
    potencia: int
    precision: int
    pp: int                                # usos del movimiento
    descripcion: str
    efecto: Optional[str] = None           # descripcion del efecto especial si lo tiene
    categoria: str = "Fisico"              # "Fisico", "Especial" o "Estado"
    objetivo: str = "Foe"                  # "Foe" (enemigo) o "Self" (uno mismo)
    siempre_acierta: bool = False          # ignora la comprobación de precisión
    prioridad: int = 0                     # orden de turno (+1 va antes, -1 va después)

    class Settings:
        name = "movimiento_catalogo"
