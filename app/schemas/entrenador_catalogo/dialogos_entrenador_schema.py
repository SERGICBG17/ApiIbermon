from pydantic import BaseModel


class DialogosEntrenadorSchema(BaseModel):
    antes: str
    victoria: str
    derrota: str
