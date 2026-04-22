from pydantic import BaseModel

class MovimientoPosibleSchema(BaseModel):
    """Movimiento que un ibermon puede aprender, con el nivel al que lo aprende."""
    numero: int
    nivel: int