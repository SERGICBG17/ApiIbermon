from datetime import datetime

from beanie import Document, PydanticObjectId
from typing import List, Dict

from app.models.partida.posicion import Posicion


class Partida(Document):
    usuario_id: PydanticObjectId
    nombre: str #nombre de la partida
    personaje_elegido: str
    starter_elegido: int | None = None             # ref a IbermonCatalogo.numero
    mapa_actual: str
    posicion: Posicion
    dinero: int = 0
    tiempo_jugado: int = 0            # en segundos
    fecha_creacion: datetime
    ultima_conexion: datetime

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
