"""
Añade a la BD el ibermon Kotlin (1004) y su movimiento AtaqueDependencias (10012).
Idempotente: si un numero ya existe en BD, lo salta.

Ejecutar:
    python -m app.utils.seed_kotlin
"""
import asyncio

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.ibermon_catalogo import IbermonCatalogo, MovimientoPosible, StatsBase
from app.models.movimiento_catalogo import MovimientoCatalogo


MOVIMIENTO_KOTLIN = {
    "numero": 10012,
    "nombre": "AtaqueDependencias",
    "tipo": "Eléctrico",
    "potencia": 100,
    "precision": 20,
    "pp": 50,
    "descripcion": "Ataque muy eficaz pero dificil de acertar",
    "efecto": None,
    "categoria": "Especial",
    "objetivo": "Foe",
    "siempre_acierta": False,
    "prioridad": 0,
}


KOTLIN = {
    "numero": 1004,
    "nombre": "Kotlin",
    "tipo1": "Eléctrico",
    "tipo2": "Dragón",
    "descripcion": "Alomejor ataca",
    "stats_base": {
        "hp": 100,
        "ataque": 50,
        "defensa": 70,
        "ataque_especial": 65,
        "defensa_especial": 65,
        "velocidad": 65,
    },
    "movimientos_posibles": [
        {"numero": 10012, "nivel": 10},
    ],
    "evoluciona_a": None,
    "nivel_evolucion": None,
    "sprite_frontal": "Kotlin/Kotlin.png",
    "sprite_trasero": "Kotlin/back/Kotlin.png",
    "catch_rate": 100,
    "exp_yield": 300,
    "growth_rate": "Rapido",
}


async def seed_movimiento_kotlin():
    existe = await MovimientoCatalogo.find_one(
        MovimientoCatalogo.numero == MOVIMIENTO_KOTLIN["numero"]
    )
    if existe:
        for campo, valor in MOVIMIENTO_KOTLIN.items():
            setattr(existe, campo, valor)
        await existe.save()
        print("  Movimiento AtaqueDependencias actualizado")
        return

    await MovimientoCatalogo(**MOVIMIENTO_KOTLIN).insert()
    print("  Movimiento AtaqueDependencias insertado")


async def seed_ibermon_kotlin():
    existe = await IbermonCatalogo.find_one(IbermonCatalogo.numero == KOTLIN["numero"])
    if existe:
        for campo, valor in KOTLIN.items():
            if campo == "stats_base":
                valor = StatsBase(**valor)
            elif campo == "movimientos_posibles":
                valor = [MovimientoPosible(**mp) for mp in valor]
            setattr(existe, campo, valor)
        await existe.save()
        print("  Ibermon Kotlin actualizado")
        return

    doc = IbermonCatalogo(
        **{
            **KOTLIN,
            "stats_base": StatsBase(**KOTLIN["stats_base"]),
            "movimientos_posibles": [
                MovimientoPosible(**mp) for mp in KOTLIN["movimientos_posibles"]
            ],
        }
    )
    await doc.insert()
    print("  Ibermon Kotlin insertado")


async def main():
    print("Seed Kotlin...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[IbermonCatalogo, MovimientoCatalogo],
    )
    await seed_movimiento_kotlin()
    await seed_ibermon_kotlin()
    print("Seed Kotlin completado")


if __name__ == "__main__":
    asyncio.run(main())
