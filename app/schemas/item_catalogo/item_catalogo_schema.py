from pydantic import BaseModel

from app.schemas.item_catalogo.efecto_item_schema import EfectoItemSchema


# --- REQUEST ---

class ItemCatalogoCrearSchema(BaseModel):
    """Para poblar la BD con los items del juego (script seed)."""
    numero: int
    nombre: str
    descripcion: str
    tipo: str
    efecto: EfectoItemSchema
    precio: int


# --- RESPONSE ---

class ItemCatalogoResumenSchema(BaseModel):
    """Vista reducida para listar items en la tienda o inventario."""
    numero: int
    nombre: str
    tipo: str
    precio: int


class ItemCatalogoDetalleSchema(BaseModel):
    """Vista completa de un item."""
    numero: int
    nombre: str
    descripcion: str
    tipo: str
    efecto: EfectoItemSchema
    precio: int
