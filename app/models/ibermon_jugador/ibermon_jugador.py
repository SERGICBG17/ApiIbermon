from beanie import Document, PydanticObjectId
from typing import List, Optional

from app.models.ibermon_jugador.movimiento_aprendido import MovimientoAprendido

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
