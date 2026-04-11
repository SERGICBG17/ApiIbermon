from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List, Optional


class MovimientoAprendido(BaseModel):
    numero: int   # ref a MovimientoCatalogo.numero
    pp: int       # PP actuales restantes del movimiento


class IbermonJugador(Document):
    partida_id: PydanticObjectId
    ibermon_catalogo_id: int                         # ref a IbermonCatalogo.numero
    nickname: Optional[str] = None
    nivel: int = 1
    experiencia: int = 0
    hp_actual: int
    ubicacion: str                                   # "equipo" o "centro"
    movimientos_aprendidos: List[MovimientoAprendido] = []  # max 4, con PP actuales

    class Settings:
        name = "ibermon_jugador"
