from pydantic import BaseModel

class StatsBaseSchema(BaseModel):
    hp: int
    ataque: int
    defensa: int
    ataque_especial: int
    defensa_especial: int
    velocidad: int