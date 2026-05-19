from typing import List

from pydantic import BaseModel


class EquipoEntrenadorSchema(BaseModel):
    numero: int
    nivel: int
    movs: List[int] = []
