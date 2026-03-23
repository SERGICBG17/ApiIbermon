from pydantic import BaseModel
from typing import Optional


# --- REQUEST ---

class MovimientoCatalogoCrearSchema(BaseModel):
    """Para poblar la BD con los movimientos del juego (script seed)."""
    numero: int
    nombre: str
    tipo: str
    potencia: int
    precision: int
    pp: int
    descripcion: str
    efecto: Optional[str] = None


# --- RESPONSE ---

class MovimientoCatalogoResumenSchema(BaseModel):
    """Vista reducida: solo lo esencial para mostrarlo en la UI."""
    numero: int
    nombre: str
    tipo: str
    potencia: int
    pp: int


class MovimientoCatalogoDetalleSchema(BaseModel):
    """Vista completa de un movimiento."""
    numero: int
    nombre: str
    tipo: str
    potencia: int
    precision: int
    pp: int
    descripcion: str
    efecto: Optional[str] = None
