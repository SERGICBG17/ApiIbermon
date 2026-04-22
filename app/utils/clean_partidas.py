"""
Borra las colecciones de jugador (partidas, ibermon, items, usuarios).
Los catalogos NO se tocan.

Ejecutar desde la raiz del proyecto:
    python -m app.utils.clean_partidas
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.usuario import Usuario
from app.models.partida.partida import Partida
from app.models.ibermon_jugador.ibermon_jugador import IbermonJugador
from app.models.item_jugador import ItemJugador


async def main():
    print("Limpiando colecciones de jugador...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[Usuario, Partida, IbermonJugador, ItemJugador],
    )

    await Usuario.delete_all()
    print("  usuarios borrados")

    await Partida.delete_all()
    print("  partidas borradas")

    await IbermonJugador.delete_all()
    print("  ibermon_jugador borrado")

    await ItemJugador.delete_all()
    print("  item_jugador borrado")

    print("Listo. Los catalogos no se han tocado.")


if __name__ == "__main__":
    asyncio.run(main())
