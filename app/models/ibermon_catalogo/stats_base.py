from pydantic import BaseModel

class StatsBase(BaseModel):
    hp: int
    ataque: int
    defensa: int
    ataque_especial: int
    defensa_especial: int
    velocidad: int