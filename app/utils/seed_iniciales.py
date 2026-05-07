"""
Añade a la BD los 3 iniciales propios (1001-1003) y sus 11 movimientos custom (10001-10011).
Idempotente: si un numero ya existe en BD, lo salta.

Ejecutar:
    python -m app.utils.seed_iniciales
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.ibermon_catalogo import IbermonCatalogo, StatsBase, MovimientoPosible
from app.models.movimiento_catalogo import MovimientoCatalogo


MOVIMIENTOS = [
    # Nenzen
    {"numero": 10001, "nombre": "Tenshoku", "tipo": "Psíquico", "potencia": 80, "precision": 100, "pp": 15, "descripcion": "Proyecta su aura a distancia. Puede atravesar el viento.", "efecto": None, "categoria": "Especial", "objetivo": "Foe", "siempre_acierta": False, "prioridad": 0},
    {"numero": 10002, "nombre": "Shu", "tipo": "Siniestro", "potencia": 0, "precision": 100, "pp": 15, "descripcion": "Envuelve al rival con su aura y lo controla durante un turno.", "efecto": "bloqueo_movimiento", "categoria": "Estado", "objetivo": "Foe", "siempre_acierta": True, "prioridad": 0},
    {"numero": 10003, "nombre": "Gyo", "tipo": "Psíquico", "potencia": 0, "precision": 100, "pp": 20, "descripcion": "Concentra su aura. Sube Defensa y Defensa Especial 1 nivel.", "efecto": "sube_def_y_defesp", "categoria": "Estado", "objetivo": "Self", "siempre_acierta": True, "prioridad": 0},
    {"numero": 10004, "nombre": "In", "tipo": "Siniestro", "potencia": 80, "precision": 100, "pp": 15, "descripcion": "Materializa su aura en una mano gigante que golpea al rival.", "efecto": None, "categoria": "Fisico", "objetivo": "Foe", "siempre_acierta": False, "prioridad": 0},

    # Kal-Noel
    {"numero": 10005, "nombre": "Visión Láser", "tipo": "Fuego", "potencia": 0, "precision": 90, "pp": 15, "descripcion": "Lanza un rayo láser. No causa daño pero provoca quemaduras.", "efecto": "quemadura", "categoria": "Estado", "objetivo": "Foe", "siempre_acierta": False, "prioridad": 0},
    {"numero": 10006, "nombre": "Redkriptonite", "tipo": "Roca", "potencia": 80, "precision": 100, "pp": 10, "descripcion": "Energía rojiza. El daño aumenta a medida que se usa.", "efecto": None, "categoria": "Especial", "objetivo": "Foe", "siempre_acierta": False, "prioridad": 0},
    {"numero": 10007, "nombre": "Ataque Rápido", "tipo": "Normal", "potencia": 40, "precision": 100, "pp": 30, "descripcion": "Ataque veloz con prioridad aumentada.", "efecto": None, "categoria": "Fisico", "objetivo": "Foe", "siempre_acierta": False, "prioridad": 1},
    {"numero": 10008, "nombre": "Golpe Meteoro", "tipo": "Roca", "potencia": 90, "precision": 90, "pp": 5, "descripcion": "Salta a gran altura y cae como un meteorito ardiente.", "efecto": None, "categoria": "Fisico", "objetivo": "Foe", "siempre_acierta": False, "prioridad": 0},

    # Antonio Recio
    {"numero": 10009, "nombre": "Centollazo", "tipo": "Agua", "potencia": 90, "precision": 100, "pp": 15, "descripcion": "El cangrejo salta sobre el rival y lo golpea con sus pinzas.", "efecto": None, "categoria": "Fisico", "objetivo": "Foe", "siempre_acierta": False, "prioridad": 0},
    {"numero": 10010, "nombre": "Azote de los Corruptos", "tipo": "Siniestro", "potencia": 95, "precision": 100, "pp": 10, "descripcion": "Aura oscura que reduce la Defensa del rival.", "efecto": "baja_defensa", "categoria": "Especial", "objetivo": "Foe", "siempre_acierta": False, "prioridad": 0},
    {"numero": 10011, "nombre": "Marea Justiciera", "tipo": "Agua", "potencia": 120, "precision": 85, "pp": 5, "descripcion": "Una gran ola arrastra al rival con la fuerza del mar.", "efecto": None, "categoria": "Fisico", "objetivo": "Foe", "siempre_acierta": False, "prioridad": 0},
]


IBERMON = [
    {
        "numero": 1001, "nombre": "Nenzen", "tipo1": "Psíquico", "tipo2": "Siniestro",
        "descripcion": "Usa su aura para materializar habilidades invisibles. Su comportamiento varía según el vínculo con su Entrenador. Habilidad: Vínculo Nen - potencia los movimientos según los PS restantes.",
        "stats_base": {"hp": 78, "ataque": 62, "defensa": 70, "ataque_especial": 128, "defensa_especial": 110, "velocidad": 117},
        "movimientos_posibles": [
            {"numero": 10001, "nivel": 1},
            {"numero": 10002, "nivel": 1},
            {"numero": 10003, "nivel": 8},
            {"numero": 10004, "nivel": 16},
        ],
        "evoluciona_a": None, "nivel_evolucion": None,
        "sprite_frontal": "Iniciales/1001.png", "sprite_trasero": "Iniciales/back/1001.png",
        "catch_rate": 45, "exp_yield": 64, "growth_rate": "Medio",
    },
    {
        "numero": 1002, "nombre": "Kal-Noel", "tipo1": "Fuego", "tipo2": "Roca",
        "descripcion": "Vino en una nave igual que su hermano, pero cayó en un volcán en lugar de en una granja. Habilidad: Coraza Ígnea - impide el daño por contacto y puede quemar al atacante.",
        "stats_base": {"hp": 95, "ataque": 120, "defensa": 110, "ataque_especial": 75, "defensa_especial": 80, "velocidad": 100},
        "movimientos_posibles": [
            {"numero": 10007, "nivel": 1},
            {"numero": 10005, "nivel": 5},
            {"numero": 10006, "nivel": 12},
            {"numero": 10008, "nivel": 20},
        ],
        "evoluciona_a": None, "nivel_evolucion": None,
        "sprite_frontal": "Iniciales/1002.png", "sprite_trasero": "Iniciales/back/1002.png",
        "catch_rate": 45, "exp_yield": 64, "growth_rate": "Medio",
    },
    {
        "numero": 1003, "nombre": "Antonio Recio", "tipo1": "Agua", "tipo2": None,
        "descripcion": "Lucha incansablemente contra la corrupción junto a su fiel cangrejo. Justiciero y severo, su palabra es ley. Habilidad: Justicia Inflexible - sube el Ataque cuando un aliado es debilitado.",
        "stats_base": {"hp": 85, "ataque": 105, "defensa": 85, "ataque_especial": 75, "defensa_especial": 85, "velocidad": 60},
        "movimientos_posibles": [
            {"numero": 10007, "nivel": 1},
            {"numero": 10009, "nivel": 5},
            {"numero": 10010, "nivel": 12},
            {"numero": 10011, "nivel": 20},
        ],
        "evoluciona_a": None, "nivel_evolucion": None,
        "sprite_frontal": "Iniciales/1003.png", "sprite_trasero": "Iniciales/back/1003.png",
        "catch_rate": 45, "exp_yield": 64, "growth_rate": "Medio",
    },
]


async def seed_movimientos_iniciales():
    nuevos = 0
    for m in MOVIMIENTOS:
        existe = await MovimientoCatalogo.find_one(MovimientoCatalogo.numero == m["numero"])
        if existe:
            continue
        await MovimientoCatalogo(**m).insert()
        nuevos += 1
    print(f"  Movimientos nuevos insertados: {nuevos}/{len(MOVIMIENTOS)}")


async def seed_ibermon_iniciales():
    nuevos = 0
    for ib in IBERMON:
        existe = await IbermonCatalogo.find_one(IbermonCatalogo.numero == ib["numero"])
        if existe:
            continue
        doc = IbermonCatalogo(**{
            **ib,
            "stats_base": StatsBase(**ib["stats_base"]),
            "movimientos_posibles": [MovimientoPosible(**mp) for mp in ib["movimientos_posibles"]],
        })
        await doc.insert()
        nuevos += 1
    print(f"  Ibermon iniciales insertados: {nuevos}/{len(IBERMON)}")


async def main():
    print("Seed iniciales...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[IbermonCatalogo, MovimientoCatalogo],
    )
    await seed_movimientos_iniciales()
    await seed_ibermon_iniciales()
    print("Seed iniciales completado")


if __name__ == "__main__":
    asyncio.run(main())
