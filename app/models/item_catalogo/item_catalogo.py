from beanie import Document

from app.models.item_catalogo.efecto_item import EfectoItem

class ItemCatalogo(Document):
    numero: int                       # PK
    nombre: str
    descripcion: str
    tipo: str                         # "curacion", "captura", "batalla", "clave"
    efecto: EfectoItem
    precio: int
    sprite_frontal: str | None = None  # URL del sprite (PokeAPI o ruta relativa)

    class Settings:
        name = "item_catalogo"
