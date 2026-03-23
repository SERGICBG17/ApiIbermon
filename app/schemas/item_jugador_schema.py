from pydantic import BaseModel


# --- REQUEST ---

class ItemJugadorAnadirSchema(BaseModel):
    """Añade un item al inventario de la partida."""
    item_catalogo_id: int
    cantidad: int = 1


class ItemJugadorActualizarSchema(BaseModel):
    """Actualiza la cantidad de un item del inventario."""
    cantidad: int


# --- RESPONSE ---

class ItemJugadorSchema(BaseModel):
    """Datos completos de un item del jugador."""
    id: str
    partida_id: str
    item_catalogo_id: int
    cantidad: int
