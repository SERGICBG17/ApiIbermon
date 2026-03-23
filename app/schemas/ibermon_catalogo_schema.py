from pydantic import BaseModel
from typing import List, Optional


# --- SUBMODELO (solo en esquemas, no en el modelo) ---

class StatsBaseSchema(BaseModel):
    hp: int
    ataque: int
    defensa: int
    ataque_especial: int
    defensa_especial: int
    velocidad: int


# --- REQUEST ---

class IbermonCatalogoCrearSchema(BaseModel):
    """Para poblar la BD con los ibermon del juego (script seed)."""
    numero: int
    nombre: str
    tipo1: str
    tipo2: Optional[str] = None
    descripcion: str
    stats_base: StatsBaseSchema           # se descompone al guardar en el modelo
    movimientos_posibles: List[int] = []
    evoluciona_a: Optional[int] = None
    nivel_evolucion: Optional[int] = None
    sprite: str


# --- RESPONSE ---

class IbermonCatalogoResumenSchema(BaseModel):
    """Vista reducida para listar todos los ibermon (pokedex publica)."""
    numero: int
    nombre: str
    tipo1: str
    tipo2: Optional[str] = None
    sprite: str


class IbermonCatalogoDetalleSchema(BaseModel):
    """Vista completa de un ibermon del catalogo."""
    numero: int
    nombre: str
    tipo1: str
    tipo2: Optional[str] = None
    descripcion: str
    hp_base: int
    ataque_base: int
    defensa_base: int
    ataque_especial_base: int
    defensa_especial_base: int
    velocidad_base: int
    movimientos_posibles: List[int] = []
    evoluciona_a: Optional[int] = None
    nivel_evolucion: Optional[int] = None
    sprite: str
