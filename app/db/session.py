from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.usuario import Usuario
from app.models.partida import Partida
from app.models.ibermon_jugador import IbermonJugador
from app.models.ibermon_catalogo import IbermonCatalogo
from app.models.movimiento_catalogo import MovimientoCatalogo
from app.models.item_catalogo import ItemCatalogo
from app.models.logro_catalogo import LogroCatalogo


async def connect_db():
    """Inicia la conexión a MongoDB y registra los modelos en Beanie."""
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[
            Usuario,
            Partida,
            IbermonJugador,
            IbermonCatalogo,
            MovimientoCatalogo,
            ItemCatalogo,
            LogroCatalogo,
        ],
    )
