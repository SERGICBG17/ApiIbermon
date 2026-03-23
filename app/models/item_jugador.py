from beanie import Document, PydanticObjectId


class ItemJugador(Document):
    partida_id: PydanticObjectId
    item_catalogo_id: int             # ref a ItemCatalogo.numero
    cantidad: int = 1

    class Settings:
        name = "item_jugador"
