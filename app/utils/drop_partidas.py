import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def drop_collection():
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # ajusta tu URI
    db = client["ibermon_db"]  # ajusta el nombre de tu DB
    await db["partidas"].drop()
    print("Colección 'partidas' eliminada")
    client.close()

asyncio.run(drop_collection())