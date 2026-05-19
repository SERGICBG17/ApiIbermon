from typing import List

from pydantic import BaseModel


class EquipoEntrenador(BaseModel):
    numero: int
    nivel: int
    movs: List[int] = []
