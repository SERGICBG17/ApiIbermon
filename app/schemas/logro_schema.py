from pydantic import BaseModel
from typing import List


# --- REQUEST ---

class LogroCatalogoCrearSchema(BaseModel):
    """Para poblar la BD con los logros del juego (script seed)."""
    codigo: str
    nombre: str
    descripcion: str
    condicion: str
    icono: str


class DesbloquearLogroSchema(BaseModel):
    """Desbloquea un logro en la partida del usuario."""
    codigo: str                       # codigo del logro a desbloquear


class ActualizarCombateSchema(BaseModel):
    """Actualiza el resultado de un combate."""
    resultado: str                    # "ganado" o "perdido"


class ActualizarPokedexSchema(BaseModel):
    """Actualiza la pokedex del jugador."""
    visto: List[int] = []
    capturado: List[int] = []


class AnadirMedallaSchema(BaseModel):
    """Anade una medalla a la partida."""
    nombre_medalla: str


# --- RESPONSE ---

class LogroCatalogoSchema(BaseModel):
    """Vista completa de un logro del catalogo."""
    codigo: str
    nombre: str
    descripcion: str
    condicion: str
    icono: str


class ProgresoSchema(BaseModel):
    """Resumen del progreso de la partida."""
    medallas: List[str] = []
    logros: List[str] = []
    pokedex_visto: List[int] = []
    pokedex_capturado: List[int] = []
    combates_ganados: int
    combates_perdidos: int
