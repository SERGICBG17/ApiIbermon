from beanie import Document
from pydantic import BaseModel
from typing import List, Optional


class StatsBase(BaseModel):
    hp: int
    ataque: int
    defensa: int
    ataque_especial: int
    defensa_especial: int
    velocidad: int


class IbermonCatalogo(Document):
    numero: int                              # PK: 1, 4, 25...
    nombre: str
    tipo1: str
    tipo2: Optional[str] = None
    descripcion: str
    stats_base: StatsBase
    movimientos_posibles: List[int] = []     # ref a MovimientoCatalogo.numero
    evoluciona_a: Optional[int] = None       # numero del ibermon al que evoluciona
    nivel_evolucion: Optional[int] = None    # None si evoluciona por piedra u otro metodo
    sprite: str                              # nombre del asset en Unity ej: "sprite_ibermon_001"

    class Settings:
        name = "ibermon_catalogo"
