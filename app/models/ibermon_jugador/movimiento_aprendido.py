from pydantic import BaseModel

class MovimientoAprendido(BaseModel):
    numero: int   # ref a MovimientoCatalogo.numero
    pp: int       # PP actuales restantes del movimiento