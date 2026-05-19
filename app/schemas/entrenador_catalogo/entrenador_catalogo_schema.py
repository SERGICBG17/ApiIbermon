from typing import List, Optional

from pydantic import BaseModel

from app.schemas.entrenador_catalogo.dialogos_entrenador_schema import DialogosEntrenadorSchema
from app.schemas.entrenador_catalogo.equipo_entrenador_schema import EquipoEntrenadorSchema


class EntrenadorCatalogoCrearSchema(BaseModel):
    """Para poblar la BD con los entrenadores del juego."""
    numero: int
    nombre: str
    equipo: List[EquipoEntrenadorSchema] = []
    recompensa: int = 0
    dialogos: DialogosEntrenadorSchema
    sprite: Optional[str] = None


class EntrenadorCatalogoResumenSchema(BaseModel):
    """Vista reducida para listar entrenadores."""
    numero: int
    nombre: str
    recompensa: int


class EntrenadorCatalogoDetalleSchema(BaseModel):
    """Vista completa de un entrenador."""
    numero: int
    nombre: str
    equipo: List[EquipoEntrenadorSchema] = []
    recompensa: int
    dialogos: DialogosEntrenadorSchema
    sprite: Optional[str] = None
