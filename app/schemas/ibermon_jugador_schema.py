from pydantic import BaseModel
from typing import List, Optional


# --- SUBMODELO ---

class MovimientoAprendidoSchema(BaseModel):
    """Movimiento conocido por un ibermon del jugador, con sus PP actuales."""
    numero: int
    pp: int


# --- REQUEST ---

class IbermonJugadorCrearSchema(BaseModel):
    """Datos para añadir un nuevo ibermon a la partida (al capturarlo)."""
    ibermon_catalogo_id: int
    nickname: Optional[str] = None
    nivel: int = 1
    hp_actual: int
    ubicacion: str = "equipo"         # por defecto va al equipo


class IbermonJugadorMoverSchema(BaseModel):
    """Mueve un ibermon entre el equipo y el centro."""
    ubicacion: str                    # "equipo" o "centro"


class IbermonJugadorActualizarSchema(BaseModel):
    """Actualiza el estado de un ibermon tras un combate o subida de nivel."""
    nivel: Optional[int] = None
    experiencia: Optional[int] = None
    hp_actual: Optional[int] = None
    movimientos_aprendidos: Optional[List[MovimientoAprendidoSchema]] = None
    nickname: Optional[str] = None


# --- RESPONSE ---

class IbermonJugadorSchema(BaseModel):
    """Datos completos de un ibermon del jugador."""
    id: str
    partida_id: str
    ibermon_catalogo_id: int
    nickname: Optional[str] = None
    nivel: int
    experiencia: int
    hp_actual: int
    ubicacion: str
    movimientos_aprendidos: List[MovimientoAprendidoSchema] = []
