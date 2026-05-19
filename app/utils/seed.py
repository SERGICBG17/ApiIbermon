"""
Seed unificado de la base de datos del juego.

Ejecutar desde la raiz del proyecto:

    python -m app.utils.seed

Orquesta los cuatro bloques de seed en orden:
  1. seed_pokeapi   -> 649 Pokemon canonicos + sus movimientos (de PokeAPI)
  2. seed_iniciales -> 3 iniciales custom + 11 movimientos custom
  3. seed_kotlin    -> Kotlin + AtaqueDependencias
  4. items + logros + entrenadores -> hardcoded en este archivo

Todas las funciones son idempotentes: si la coleccion ya tiene datos, se omite.
Si quieres re-seedear desde cero, usa clean.py primero.
"""
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.item_catalogo import ItemCatalogo, EfectoItem
from app.models.logro_catalogo import LogroCatalogo
from app.models.entrenador_catalogo import EntrenadorCatalogo, EquipoEntrenador, DialogosEntrenador

from app.utils import seed_pokeapi, seed_iniciales, seed_kotlin


# ──────────────────────────────────────────
# ITEMS
# ──────────────────────────────────────────
# Sprites tomados del CDN publico de PokeAPI
_SPRITE_BASE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items"

ITEMS = [
    {"numero": 1,  "nombre": "Pocion",        "descripcion": "Restaura 20 HP.",                          "tipo": "curacion", "efecto": {"tipo_efecto": "curacion_hp",    "valor": 20},            "precio": 300,  "sprite_frontal": f"{_SPRITE_BASE}/potion.png"},
    {"numero": 2,  "nombre": "Super Pocion",  "descripcion": "Restaura 50 HP.",                          "tipo": "curacion", "efecto": {"tipo_efecto": "curacion_hp",    "valor": 50},            "precio": 700,  "sprite_frontal": f"{_SPRITE_BASE}/super-potion.png"},
    {"numero": 3,  "nombre": "Hiper Pocion",  "descripcion": "Restaura 200 HP.",                         "tipo": "curacion", "efecto": {"tipo_efecto": "curacion_hp",    "valor": 200},           "precio": 1200, "sprite_frontal": f"{_SPRITE_BASE}/hyper-potion.png"},
    {"numero": 4,  "nombre": "Pocion Maxima", "descripcion": "Restaura todos los HP.",                   "tipo": "curacion", "efecto": {"tipo_efecto": "curacion_hp",    "valor": 9999},          "precio": 2500, "sprite_frontal": f"{_SPRITE_BASE}/max-potion.png"},
    {"numero": 5,  "nombre": "Antidoto",      "descripcion": "Cura el envenenamiento.",                  "tipo": "curacion", "efecto": {"tipo_efecto": "cura_veneno",    "valor": None},          "precio": 100,  "sprite_frontal": f"{_SPRITE_BASE}/antidote.png"},
    {"numero": 6,  "nombre": "Quemasal",      "descripcion": "Cura la quemadura.",                       "tipo": "curacion", "efecto": {"tipo_efecto": "cura_quemadura", "valor": None},          "precio": 250,  "sprite_frontal": f"{_SPRITE_BASE}/burn-heal.png"},
    {"numero": 7,  "nombre": "Paralyzer",     "descripcion": "Cura la paralisis.",                       "tipo": "curacion", "efecto": {"tipo_efecto": "cura_paralisis", "valor": None},          "precio": 200,  "sprite_frontal": f"{_SPRITE_BASE}/paralyze-heal.png"},
    {"numero": 8,  "nombre": "Revivir",       "descripcion": "Revive con la mitad de HP.",               "tipo": "curacion", "efecto": {"tipo_efecto": "revivir",        "valor": 0.5},           "precio": 1500, "sprite_frontal": f"{_SPRITE_BASE}/revive.png"},
    {"numero": 9,  "nombre": "Revivir Max",   "descripcion": "Revive con todos los HP.",                 "tipo": "curacion", "efecto": {"tipo_efecto": "revivir",        "valor": 1.0},           "precio": 4000, "sprite_frontal": f"{_SPRITE_BASE}/max-revive.png"},
    {"numero": 10, "nombre": "Iberball",      "descripcion": "Bola de captura basica.",                  "tipo": "captura",  "efecto": {"tipo_efecto": "captura",        "valor": 1.0},           "precio": 200,  "sprite_frontal": f"{_SPRITE_BASE}/poke-ball.png"},
    {"numero": 11, "nombre": "Super Ball",    "descripcion": "Mejor tasa de captura.",                   "tipo": "captura",  "efecto": {"tipo_efecto": "captura",        "valor": 1.5},           "precio": 600,  "sprite_frontal": f"{_SPRITE_BASE}/great-ball.png"},
    {"numero": 12, "nombre": "Ultra Ball",    "descripcion": "Alta tasa de captura.",                    "tipo": "captura",  "efecto": {"tipo_efecto": "captura",        "valor": 2.0},           "precio": 1200, "sprite_frontal": f"{_SPRITE_BASE}/ultra-ball.png"},
    {"numero": 13, "nombre": "Master Ball",   "descripcion": "Captura cualquier ibermon sin fallo.",      "tipo": "captura",  "efecto": {"tipo_efecto": "captura",        "valor": 255},           "precio": 0,    "sprite_frontal": f"{_SPRITE_BASE}/master-ball.png"},
    {"numero": 14, "nombre": "X Ataque",      "descripcion": "Sube el ataque en combate.",               "tipo": "batalla",  "efecto": {"tipo_efecto": "subir_ataque",   "valor": 1},             "precio": 500,  "sprite_frontal": f"{_SPRITE_BASE}/x-attack.png"},
    {"numero": 15, "nombre": "X Defensa",     "descripcion": "Sube la defensa en combate.",              "tipo": "batalla",  "efecto": {"tipo_efecto": "subir_defensa",  "valor": 1},             "precio": 550,  "sprite_frontal": f"{_SPRITE_BASE}/x-defense.png"},
    {"numero": 16, "nombre": "X Velocidad",   "descripcion": "Sube la velocidad en combate.",            "tipo": "batalla",  "efecto": {"tipo_efecto": "subir_velocidad","valor": 1},             "precio": 350,  "sprite_frontal": f"{_SPRITE_BASE}/x-speed.png"},
    {"numero": 17, "nombre": "Mochila Vieja", "descripcion": "Una mochila abandonada. Abre una puerta.", "tipo": "clave",    "efecto": {"tipo_efecto": "clave",          "valor": "puerta_cueva_1"},"precio": 0,  "sprite_frontal": None},
    {"numero": 18, "nombre": "Llave del Gym", "descripcion": "Llave del gimnasio principal.",            "tipo": "clave",    "efecto": {"tipo_efecto": "clave",          "valor": "gym_1"},       "precio": 0,    "sprite_frontal": None},
]


# ──────────────────────────────────────────
# LOGROS
# ──────────────────────────────────────────
LOGROS = [
    {"codigo": "primer_paso",        "nombre": "Primer paso",         "descripcion": "Comienza tu aventura.",                        "condicion": "nueva_partida_creada",       "icono": "logro_inicio"},
    {"codigo": "primer_combate",     "nombre": "Primera batalla",     "descripcion": "Gana tu primer combate.",                      "condicion": "combates_ganados >= 1",      "icono": "logro_espada"},
    {"codigo": "primera_captura",    "nombre": "Capturador",          "descripcion": "Captura tu primer ibermon.",                   "condicion": "pokedex_capturado >= 1",     "icono": "logro_iberball"},
    {"codigo": "primera_medalla",    "nombre": "Primera medalla",     "descripcion": "Consigue tu primera medalla de gimnasio.",     "condicion": "medallas >= 1",              "icono": "logro_medalla"},
    {"codigo": "captura_5",          "nombre": "Coleccionista",       "descripcion": "Captura 5 ibermon diferentes.",                "condicion": "pokedex_capturado >= 5",     "icono": "logro_coleccion"},
    {"codigo": "captura_10",         "nombre": "Gran Coleccionista",  "descripcion": "Captura 10 ibermon diferentes.",               "condicion": "pokedex_capturado >= 10",    "icono": "logro_coleccion2"},
    {"codigo": "equipo_completo",    "nombre": "Equipo al completo",  "descripcion": "Ten 6 ibermon en tu equipo a la vez.",         "condicion": "equipo == 6",                "icono": "logro_equipo"},
    {"codigo": "diez_victorias",     "nombre": "Veterano",            "descripcion": "Gana 10 combates.",                           "condicion": "combates_ganados >= 10",     "icono": "logro_veterano"},
    {"codigo": "cincuenta_victorias","nombre": "Maestro Luchador",    "descripcion": "Gana 50 combates.",                           "condicion": "combates_ganados >= 50",     "icono": "logro_maestro_lucha"},
    {"codigo": "sin_derrotas",       "nombre": "Invicto",             "descripcion": "Gana 10 combates seguidos sin perder.",        "condicion": "racha_victorias >= 10",      "icono": "logro_invicto"},
    {"codigo": "tres_medallas",      "nombre": "Aspirante",           "descripcion": "Consigue 3 medallas de gimnasio.",             "condicion": "medallas >= 3",              "icono": "logro_medalla3"},
    {"codigo": "todas_medallas",     "nombre": "Campeon Regional",    "descripcion": "Consigue todas las medallas de gimnasio.",     "condicion": "medallas == total_gyms",     "icono": "logro_campeon"},
    {"codigo": "pokedex_completa",   "nombre": "Maestro Ibermon",     "descripcion": "Captura todos los ibermon del juego.",         "condicion": "pokedex_capturado == total", "icono": "logro_maestro"},
    {"codigo": "explorador",         "nombre": "Explorador",          "descripcion": "Visita todos los mapas del juego.",            "condicion": "mapas_visitados == total",   "icono": "logro_mapa"},
]


# ──────────────────────────────────────────
# ENTRENADORES
# ──────────────────────────────────────────
ENTRENADORES = [
    {
        "numero": 1,
        "nombre": "Paloma",
        "equipo": [
            {"numero": 1004, "nivel": 12, "movs": [10012]},
        ],
        "recompensa": 500,
        "dialogos": {
            "antes": "Luchemos!",
            "victoria": "Aun me queda mucho que aprender.",
            "derrota": "Nadie escapa de mi vista.",
        },
        "sprite": None,
    },
]


# ──────────────────────────────────────────
# SEEDERS LOCALES (items y logros)
# ──────────────────────────────────────────

async def seed_items():
    count = await ItemCatalogo.count()
    if count > 0:
        print(f"  Ya hay {count} items, omitiendo...")
        return
    await ItemCatalogo.insert_many([
        ItemCatalogo(**{**it, "efecto": EfectoItem(**it["efecto"])})
        for it in ITEMS
    ])
    print(f"  {len(ITEMS)} items insertados")


async def seed_logros():
    count = await LogroCatalogo.count()
    if count > 0:
        print(f"  Ya hay {count} logros, omitiendo...")
        return
    await LogroCatalogo.insert_many([LogroCatalogo(**l) for l in LOGROS])
    print(f"  {len(LOGROS)} logros insertados")


async def seed_entrenadores():
    creados = 0
    actualizados = 0

    for ent in ENTRENADORES:
        existente = await EntrenadorCatalogo.find_one(EntrenadorCatalogo.numero == ent["numero"])
        equipo = [EquipoEntrenador(**e) for e in ent["equipo"]]
        dialogos = DialogosEntrenador(**ent["dialogos"])

        if existente:
            existente.nombre = ent["nombre"]
            existente.equipo = equipo
            existente.recompensa = ent["recompensa"]
            existente.dialogos = dialogos
            existente.sprite = ent.get("sprite")
            await existente.save()
            actualizados += 1
            continue

        await EntrenadorCatalogo(
            numero=ent["numero"],
            nombre=ent["nombre"],
            equipo=equipo,
            recompensa=ent["recompensa"],
            dialogos=dialogos,
            sprite=ent.get("sprite"),
        ).insert()
        creados += 1

    print(f"  {creados} entrenadores insertados, {actualizados} actualizados")


# ──────────────────────────────────────────
# ORQUESTADOR
# ──────────────────────────────────────────

async def main():
    print("=== Seed unificado ===\n")

    # 1. Pokemon canonicos + movimientos via PokeAPI
    print("[1/4] Pokemon canonicos y movimientos (PokeAPI)...")
    await seed_pokeapi.main(1, 649, False)

    # 2. Iniciales custom (Nenzen, Kal-Noel, Antonio Recio)
    print("\n[2/4] Iniciales custom...")
    await seed_iniciales.main()

    # 3. Kotlin custom
    print("\n[3/4] Kotlin custom...")
    await seed_kotlin.main()

    # 4. Items, logros y entrenadores (datos locales)
    print("\n[4/4] Items, logros y entrenadores...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[ItemCatalogo, LogroCatalogo, EntrenadorCatalogo],
    )
    await seed_items()
    await seed_logros()
    await seed_entrenadores()

    print("\n=== Seed completado ===")


if __name__ == "__main__":
    asyncio.run(main())
