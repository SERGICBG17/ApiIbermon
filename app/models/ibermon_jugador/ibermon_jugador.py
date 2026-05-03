from beanie import Document, PydanticObjectId
from typing import List, Optional

from app.models.ibermon_jugador.movimiento_aprendido import MovimientoAprendido

class IbermonJugador(Document):
    partida_id: PydanticObjectId
    ibermon_catalogo_id: int                         # ref a IbermonCatalogo.numero
    nickname: Optional[str] = None
    nivel: int = 1                                   # en Unity: Level
    experiencia: int = 0                             # en Unity: Exp
    hp_actual: int                                   # en Unity: HP
    hp_maximo: int                                   # en Unity: MaxHp
    ubicacion: str                                   # "equipo" o "centro"
    movimientos_aprendidos: List[MovimientoAprendido] = []  # max 4, con PP actuales

    class Settings:
        name = "ibermon_jugador"
