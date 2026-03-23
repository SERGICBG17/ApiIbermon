"""
Script para borrar las colecciones de catalogos antes de hacer el seed.
Ejecutar desde la raiz del proyecto:

    python -m data.clean
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.ibermon_catalogo import IbermonCatalogo
from app.models.movimiento_catalogo import MovimientoCatalogo
from app.models.item_catalogo import ItemCatalogo
from app.models.logro_catalogo import LogroCatalogo


async def main():
    print("Limpiando colecciones de catalogos...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[IbermonCatalogo, MovimientoCatalogo, ItemCatalogo, LogroCatalogo],
    )

    await IbermonCatalogo.delete_all()
    print("  ibermon_catalogo borrado")

    await MovimientoCatalogo.delete_all()
    print("  movimiento_catalogo borrado")

    await ItemCatalogo.delete_all()
    print("  item_catalogo borrado")

    await LogroCatalogo.delete_all()
    print("  logro_catalogo borrado")

    print("Listo. Ahora ejecuta: python -m data.seed")


if __name__ == "__main__":
    asyncio.run(main())
