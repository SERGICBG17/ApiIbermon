from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List, Dict


class Posicion(BaseModel):
    x: float
    y: float


class Partida(Document):
    usuario_id: PydanticObjectId
    personaje_elegido: str
    starter_elegido: int              # ref a IbermonCatalogo.numero
    mapa_actual: str
    posicion: Posicion
    dinero: int = 0
    tiempo_jugado: int = 0            # en segundos

    # Ibermon — referencias a IbermonJugador._id
    equipo: List[PydanticObjectId] = []          # max 6
    centro_ibermon: List[PydanticObjectId] = []  # sin limite

    # Pokedex
    pokedex_visto: List[int] = []
    pokedex_capturado: List[int] = []

    # Progreso
    medallas: List[str] = []
    logros: List[str] = []
    combates_ganados: int = 0
    combates_perdidos: int = 0

    # Flags del mundo
    flags: Dict[str, bool] = {}

    class Settings:
        name = "partidas"
