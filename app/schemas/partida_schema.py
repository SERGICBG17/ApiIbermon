from pydantic import BaseModel
from typing import List, Dict, Optional
from bson import ObjectId


# --- SUBMODELOS COMPARTIDOS ---

class PosicionSchema(BaseModel):
    x: float
    y: float


class ItemInventarioSchema(BaseModel):
    item_catalogo_id: int
    cantidad: int


# --- REQUEST ---

class PartidaNuevaSchema(BaseModel):
    """Datos para crear una nueva partida."""
    personaje_elegido: str
    starter_elegido: int              # numero del ibermon inicial


class GuardarPartidaSchema(BaseModel):
    """Datos para guardar el estado completo de la partida."""
    mapa_actual: str
    posicion: PosicionSchema
    dinero: int
    tiempo_jugado: int
    inventario: List[ItemInventarioSchema] = []
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
    """Resumen de una partida para listarlas (sin todo el detalle)."""
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
    equipo: List[str] = []            # ids de IbermonJugador
    centro_ibermon: List[str] = []    # ids de IbermonJugador
    inventario: List[ItemInventarioSchema] = []
    pokedex_visto: List[int] = []
    pokedex_capturado: List[int] = []
    medallas: List[str] = []
    logros: List[str] = []
    combates_ganados: int
    combates_perdidos: int
    flags: Dict[str, bool] = {}
