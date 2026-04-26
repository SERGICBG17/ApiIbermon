from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

from app.schemas.partida.posicion_schema import PosicionSchema

class PartidaNuevaSchema(BaseModel):
    """Datos para crear una nueva partida."""
    nombre: str
    personaje_elegido: str
    fecha_creacion: datetime |None=datetime.now()

class ElegirStarterSchema(BaseModel):
    starter_elegido: int

class GuardarPartidaSchema(BaseModel):
    """Datos para guardar el estado completo de la partida."""
    mapa_actual: str
    posicion: PosicionSchema
    dinero: int
    tiempo_jugado: int
    ultima_conexion: datetime |None=datetime.now()
    pokedex_visto: List[int] = []
    pokedex_capturado: List[int] = []
    medallas: List[str] = []
    logros: List[str] = []
    combates_ganados: int
    combates_perdidos: int
    flags: Dict[str, bool] = {}


class ActualizarPosicionSchema(BaseModel):
    """Actualiza solo la posicion, el mapa actual, el tiempo jugado y la ultima conexion."""
    mapa_actual: str
    posicion: PosicionSchema
    tiempo_jugado: int
    ultima_conexion: datetime | None = None


class PartidaResumenSchema(BaseModel):
    """Resumen de una partida para listarlas."""
    id: str
    nombre: str
    personaje_elegido: str
    mapa_actual: str
    tiempo_jugado: int
    medallas: List[str] = []
    combates_ganados: int
    combates_perdidos: int
    fecha_creacion: datetime | None = None
    ultima_conexion: datetime | None = None


class PartidaCompletaSchema(BaseModel):
    """Estado completo de la partida."""
    id: str
    usuario_id: str
    personaje_elegido: str
    starter_elegido: int | None = None
    mapa_actual: str
    posicion: PosicionSchema
    dinero: int
    tiempo_jugado: int
    fecha_creacion: datetime
    ultima_conexion: datetime
    equipo: List[str] = []
    centro_ibermon: List[str] = []
    pokedex_visto: List[int] = []
    pokedex_capturado: List[int] = []
    medallas: List[str] = []
    logros: List[str] = []
    combates_ganados: int
    combates_perdidos: int
    flags: Dict[str, bool] = {}
