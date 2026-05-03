from beanie import Document
from typing import List, Optional

from app.models.ibermon_catalogo.movimiento_posible import MovimientoPosible
from app.models.ibermon_catalogo.stats_base import StatsBase


class IbermonCatalogo(Document):
    numero: int                                      # PK: 1, 4, 25...
    nombre: str
    tipo1: str
    tipo2: Optional[str] = None
    descripcion: str
    stats_base: StatsBase
    movimientos_posibles: List[MovimientoPosible] = []
    evoluciona_a: Optional[int] = None               # numero del ibermon al que evoluciona
    nivel_evolucion: Optional[int] = None            # None si evoluciona por piedra u otro metodo
    sprite_frontal: str                              # ruta del sprite frontal. en Unity: frontSprite
    sprite_trasero: str                              # ruta del sprite trasero. en Unity: backSprite
    catch_rate: int = 255                            # tasa de captura (0-255)
    exp_yield: int = 100                             # experiencia base que da al ser derrotado
    growth_rate: str = "Medio"                       # curva de crecimiento: "Medio" o "Rapido"

    class Settings:
        name = "ibermon_catalogo"
