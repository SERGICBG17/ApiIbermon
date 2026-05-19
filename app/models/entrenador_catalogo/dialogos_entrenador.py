from pydantic import BaseModel


class DialogosEntrenador(BaseModel):
    antes: str
    victoria: str
    derrota: str
