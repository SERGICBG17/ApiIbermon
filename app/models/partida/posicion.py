from pydantic import BaseModel

class Posicion(BaseModel):
    x: float
    y: float