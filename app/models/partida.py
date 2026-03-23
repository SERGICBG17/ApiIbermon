from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List, Dict


class Posicion(BaseModel):
    x: float
    y: float


class ItemInventario(BaseModel):
    item_catalogo_id: int             # ref a ItemCatalogo.numero
    cantidad: int


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

    # Inventario embebido directamente en la partida
    inventario: List[ItemInventario] = []

    # Pokedex
    pokedex_visto: List[int] = []     # numeros de IbermonCatalogo
    pokedex_capturado: List[int] = [] # numeros de IbermonCatalogo

    # Progreso
    medallas: List[str] = []
    logros: List[str] = []            # codigos de LogroCatalogo
    combates_ganados: int = 0
    combates_perdidos: int = 0

    # Flags del mundo: cofres abiertos, NPCs hablados, eventos completados
    flags: Dict[str, bool] = {}

    class Settings:
        name = "partidas"
