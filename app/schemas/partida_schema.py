from pydantic import BaseModel
from typing import List, Dict, Optional


# --- SUBMODELOS ---

class PosicionSchema(BaseModel):
    x: float
    y: float


# --- REQUEST ---

class PartidaNuevaSchema(BaseModel):
    """Datos para crear una nueva partida."""
    personaje_elegido: str
    starter_elegido: int


class GuardarPartidaSchema(BaseModel):
    """Datos para guardar el estado completo de la partida."""
    mapa_actual: str
    posicion: PosicionSchema
    dinero: int
    tiempo_jugado: int
    pokedex_visto: List[int] = []
    pokedex_capturado: List[int] = []
    medallas: List[str] = []
    logros: List[str] = []
    combates_ganados: int
    combates_perdidos: int
    flags: Dict[str, bool] = {}


class ActualizarPosicionSchema(BaseModel):
    """Actualiza solo la posicion y el mapa actual."""
    mapa_actual: str
    posicion: PosicionSchema


# --- RESPONSE ---

class PartidaResumenSchema(BaseModel):
    """Resumen de una partida para listarlas."""
    id: str
    personaje_elegido: str
    mapa_actual: str
    tiempo_jugado: int
    medallas: List[str] = []
    combates_ganados: int
    combates_perdidos: int


class PartidaCompletaSchema(BaseModel):
    """Estado completo de la partida."""
    id: str
    usuario_id: str
    personaje_elegido: str
    starter_elegido: int
    mapa_actual: str
    posicion: PosicionSchema
    dinero: int
    tiempo_jugado: int
    equipo: List[str] = []
    centro_ibermon: List[str] = []
    pokedex_visto: List[int] = []
    pokedex_capturado: List[int] = []
    medallas: List[str] = []
    logros: List[str] = []
    combates_ganados: int
    combates_perdidos: int
    flags: Dict[str, bool] = {}
