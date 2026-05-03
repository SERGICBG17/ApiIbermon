from pydantic import BaseModel, model_validator
from typing import Any, List, Optional

from app.schemas.ibermon_catalogo.movimiento_posible_schema import MovimientoPosibleSchema
from app.schemas.ibermon_catalogo.stats_base import StatsBaseSchema


# --- REQUEST ---

class IbermonCatalogoCrearSchema(BaseModel):
    """Para poblar la BD con los ibermon del juego (script seed)."""
    numero: int
    nombre: str
    tipo1: str
    tipo2: Optional[str] = None
    descripcion: str
    stats_base: StatsBaseSchema           # se descompone al guardar en el modelo
    movimientos_posibles: List[MovimientoPosibleSchema] = []
    evoluciona_a: Optional[int] = None
    nivel_evolucion: Optional[int] = None
    sprite_frontal: str
    sprite_trasero: str
    catch_rate: int = 255
    exp_yield: int = 100
    growth_rate: str = "Medio"


# --- RESPONSE ---

class IbermonCatalogoResumenSchema(BaseModel):
    """Vista reducida para listar todos los ibermon (pokedex publica)."""
    numero: int
    nombre: str
    tipo1: str
    tipo2: Optional[str] = None
    sprite_frontal: str
    sprite_trasero: str


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
    movimientos_posibles: List[MovimientoPosibleSchema] = []
    evoluciona_a: Optional[int] = None
    nivel_evolucion: Optional[int] = None
    sprite_frontal: str
    sprite_trasero: str
    catch_rate: int = 255
    exp_yield: int = 100
    growth_rate: str = "Medio"

    @model_validator(mode="before")
    @classmethod
    def _flatten_stats_base(cls, data: Any) -> Any:
        """Convierte stats_base anidado del modelo Beanie a campos planos del schema."""
        # Documento Beanie (objeto con atributos)
        if hasattr(data, "stats_base"):
            s = data.stats_base
            return {
                "numero":               data.numero,
                "nombre":               data.nombre,
                "tipo1":                data.tipo1,
                "tipo2":                data.tipo2,
                "descripcion":          data.descripcion,
                "hp_base":              s.hp,
                "ataque_base":          s.ataque,
                "defensa_base":         s.defensa,
                "ataque_especial_base": s.ataque_especial,
                "defensa_especial_base":s.defensa_especial,
                "velocidad_base":       s.velocidad,
                "movimientos_posibles": data.movimientos_posibles,
                "evoluciona_a":         data.evoluciona_a,
                "nivel_evolucion":      data.nivel_evolucion,
                "sprite_frontal":       data.sprite_frontal,
                "sprite_trasero":       data.sprite_trasero,
                "catch_rate":           data.catch_rate,
                "exp_yield":            data.exp_yield,
                "growth_rate":          data.growth_rate,
            }
        # Dict con stats_base anidado (ej: tests)
        if isinstance(data, dict) and "stats_base" in data:
            s = data.pop("stats_base")
            if isinstance(s, dict):
                data["hp_base"]               = s["hp"]
                data["ataque_base"]           = s["ataque"]
                data["defensa_base"]          = s["defensa"]
                data["ataque_especial_base"]  = s["ataque_especial"]
                data["defensa_especial_base"] = s["defensa_especial"]
                data["velocidad_base"]        = s["velocidad"]
        return data
