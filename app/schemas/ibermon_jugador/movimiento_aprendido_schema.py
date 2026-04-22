from pydantic import BaseModel

class MovimientoAprendidoSchema(BaseModel):
    """Movimiento conocido por un ibermon del jugador, con sus PP actuales."""
    numero: int
    pp: int