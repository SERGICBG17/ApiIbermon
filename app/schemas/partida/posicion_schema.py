from pydantic import BaseModel

class PosicionSchema(BaseModel):
    x: float
    y: float