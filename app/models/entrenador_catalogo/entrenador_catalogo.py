from typing import List, Optional

from beanie import Document

from app.models.entrenador_catalogo.dialogos_entrenador import DialogosEntrenador
from app.models.entrenador_catalogo.equipo_entrenador import EquipoEntrenador


class EntrenadorCatalogo(Document):
    numero: int
    nombre: str
    equipo: List[EquipoEntrenador] = []
    recompensa: int = 0
    dialogos: DialogosEntrenador
    sprite: Optional[str] = None

    class Settings:
        name = "entrenador_catalogo"
