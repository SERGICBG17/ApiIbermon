from pydantic import BaseModel

class MovimientoPosible(BaseModel):
    numero: int   # ref a MovimientoCatalogo.numero
    nivel: int    # nivel mínimo al que el ibermon aprende el movimiento