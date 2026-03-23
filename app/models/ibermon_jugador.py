from beanie import Document, PydanticObjectId
from typing import List, Optional


class IbermonJugador(Document):
    partida_id: PydanticObjectId
    ibermon_catalogo_id: int          # ref a IbermonCatalogo.numero
    nickname: Optional[str] = None
    nivel: int = 1
    experiencia: int = 0
    hp_actual: int
    ubicacion: str                    # "equipo" o "centro"
    movimientos_aprendidos: List[int] = []  # ref a MovimientoCatalogo.numero (max 4)

    class Settings:
        name = "ibermon_jugador"
