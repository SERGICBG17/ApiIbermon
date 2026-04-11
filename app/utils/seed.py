"""
Script para poblar la base de datos con los datos iniciales del juego.
Ejecutar una sola vez desde la raiz del proyecto:

    python -m app.utils.seed

Si ya hay datos y quieres re-seedear, borra la colección primero o usa clean.py.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.ibermon_catalogo import IbermonCatalogo, StatsBase, MovimientoPosible
from app.models.movimiento_catalogo import MovimientoCatalogo
from app.models.item_catalogo import ItemCatalogo, EfectoItem
from app.models.logro_catalogo import LogroCatalogo


# ──────────────────────────────────────────
# MOVIMIENTOS
# categoria: "Fisico" | "Especial" | "Estado"
# objetivo:  "Foe"    | "Self"
# ──────────────────────────────────────────
MOVIMIENTOS = [
    {"numero": 1,  "nombre": "Placaje",       "tipo": "Normal",    "potencia": 40,  "precision": 100, "pp": 35, "descripcion": "Ataque fisico basico.",                      "efecto": None,             "categoria": "Fisico",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 2,  "nombre": "Aranazo",        "tipo": "Normal",    "potencia": 40,  "precision": 100, "pp": 35, "descripcion": "Arana al rival con las garras.",             "efecto": None,             "categoria": "Fisico",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 3,  "nombre": "Grunido",        "tipo": "Normal",    "potencia": 0,   "precision": 100, "pp": 40, "descripcion": "Baja el ataque del rival 1 nivel.",          "efecto": "baja_ataque",    "categoria": "Estado",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 4,  "nombre": "Latigo",         "tipo": "Normal",    "potencia": 0,   "precision": 100, "pp": 30, "descripcion": "Baja la defensa del rival 1 nivel.",         "efecto": "baja_defensa",   "categoria": "Estado",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 5,  "nombre": "Ataque Rapido",  "tipo": "Normal",    "potencia": 40,  "precision": 100, "pp": 30, "descripcion": "Ataque con prioridad aumentada.",            "efecto": None,             "categoria": "Fisico",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 1},
    {"numero": 6,  "nombre": "Ascuas",         "tipo": "Fuego",     "potencia": 40,  "precision": 100, "pp": 25, "descripcion": "Lanza llamas. Puede quemar.",                "efecto": "quemadura_10",   "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 7,  "nombre": "Pantalla Humo",  "tipo": "Fuego",     "potencia": 0,   "precision": 100, "pp": 20, "descripcion": "Baja la precision del rival.",               "efecto": "baja_precision", "categoria": "Estado",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 8,  "nombre": "Lanzallamas",    "tipo": "Fuego",     "potencia": 90,  "precision": 100, "pp": 15, "descripcion": "Potente ataque de fuego. Puede quemar.",      "efecto": "quemadura_10",   "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 9,  "nombre": "Rueda de Fuego", "tipo": "Fuego",     "potencia": 60,  "precision": 85,  "pp": 25, "descripcion": "Envuelve al rival en llamas.",               "efecto": "quemadura_10",   "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 10, "nombre": "Pistola Agua",   "tipo": "Agua",      "potencia": 40,  "precision": 100, "pp": 25, "descripcion": "Dispara un chorro de agua.",                 "efecto": None,             "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 11, "nombre": "Cola",           "tipo": "Agua",      "potencia": 0,   "precision": 100, "pp": 30, "descripcion": "Baja la defensa del rival.",                 "efecto": "baja_defensa",   "categoria": "Estado",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 12, "nombre": "Hidrobomba",     "tipo": "Agua",      "potencia": 110, "precision": 80,  "pp": 5,  "descripcion": "Disparo de agua devastador.",                "efecto": None,             "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 13, "nombre": "Surf",           "tipo": "Agua",      "potencia": 90,  "precision": 100, "pp": 15, "descripcion": "Ola que golpea al rival.",                   "efecto": None,             "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 14, "nombre": "Latigo Cepa",    "tipo": "Planta",    "potencia": 45,  "precision": 100, "pp": 25, "descripcion": "Golpea con enredaderas.",                    "efecto": None,             "categoria": "Fisico",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 15, "nombre": "Hoja Afilada",   "tipo": "Planta",    "potencia": 55,  "precision": 95,  "pp": 25, "descripcion": "Lanza hojas cortantes al rival.",            "efecto": None,             "categoria": "Fisico",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 16, "nombre": "Rayo Solar",     "tipo": "Planta",    "potencia": 120, "precision": 100, "pp": 10, "descripcion": "Carga un turno y lanza un rayo de luz.",     "efecto": "carga_turno",    "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 17, "nombre": "Polvo Veneno",   "tipo": "Planta",    "potencia": 0,   "precision": 75,  "pp": 35, "descripcion": "Envenena al rival.",                         "efecto": "veneno",         "categoria": "Estado",   "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 18, "nombre": "Impactrueno",    "tipo": "Electrico", "potencia": 40,  "precision": 100, "pp": 30, "descripcion": "Descarga electrica. Puede paralizar.",        "efecto": "paralisis_10",   "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 19, "nombre": "Trueno",         "tipo": "Electrico", "potencia": 110, "precision": 70,  "pp": 10, "descripcion": "Gran descarga electrica. Puede paralizar.",   "efecto": "paralisis_30",   "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
    {"numero": 20, "nombre": "Rayo",           "tipo": "Electrico", "potencia": 90,  "precision": 100, "pp": 15, "descripcion": "Rayo electrico preciso. Puede paralizar.",    "efecto": "paralisis_10",   "categoria": "Especial", "objetivo": "Foe",  "siempre_acierta": False, "prioridad": 0},
]


# ──────────────────────────────────────────────────────────────────────────────
# IBERMON
# movimientos_posibles: [{numero, nivel}]  → nivel mínimo para aprender el movimiento
# catch_rate: 0-255  (45 = difícil, 255 = muy fácil)
# exp_yield:  experiencia base que da al ser derrotado
# growth_rate: "Medio" | "Rapido"
# ──────────────────────────────────────────────────────────────────────────────
IBERMON = [
    # ── Bulbasaur line ──────────────────────────────────────────────────────────
    {
        "numero": 1,  "nombre": "Bulbasaur",  "tipo1": "Planta",  "tipo2": "Veneno",
        "descripcion": "Lleva una semilla en su espalda desde que nace. La semilla crece poco a poco.",
        "stats_base": {"hp": 45, "ataque": 49, "defensa": 49, "ataque_especial": 65, "defensa_especial": 65, "velocidad": 45},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 3, "nivel": 1}, {"numero": 14, "nivel": 7}, {"numero": 17, "nivel": 13}],
        "evoluciona_a": 2, "nivel_evolucion": 16, "sprite": "sprite_ibermon_001",
        "catch_rate": 45, "exp_yield": 64, "growth_rate": "Medio",
    },
    {
        "numero": 2,  "nombre": "Ivysaur",    "tipo1": "Planta",  "tipo2": "Veneno",
        "descripcion": "La semilla de su espalda absorbe la luz solar y crece. Su aroma calma las emociones.",
        "stats_base": {"hp": 60, "ataque": 62, "defensa": 63, "ataque_especial": 80, "defensa_especial": 80, "velocidad": 60},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 14, "nivel": 1}, {"numero": 15, "nivel": 22}, {"numero": 17, "nivel": 29}],
        "evoluciona_a": 3, "nivel_evolucion": 32, "sprite": "sprite_ibermon_002",
        "catch_rate": 45, "exp_yield": 141, "growth_rate": "Medio",
    },
    {
        "numero": 3,  "nombre": "Venusaur",   "tipo1": "Planta",  "tipo2": "Veneno",
        "descripcion": "La flor de su espalda absorbe la luz solar. Su aroma tranquiliza y sana.",
        "stats_base": {"hp": 80, "ataque": 82, "defensa": 83, "ataque_especial": 100, "defensa_especial": 100, "velocidad": 80},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 15, "nivel": 1}, {"numero": 17, "nivel": 1}, {"numero": 16, "nivel": 40}],
        "evoluciona_a": None, "nivel_evolucion": None, "sprite": "sprite_ibermon_003",
        "catch_rate": 45, "exp_yield": 236, "growth_rate": "Medio",
    },
    # ── Charmander line ─────────────────────────────────────────────────────────
    {
        "numero": 4,  "nombre": "Charmander", "tipo1": "Fuego",   "tipo2": None,
        "descripcion": "La llama de su cola indica su estado de animo. Arde con mas fuerza en combate.",
        "stats_base": {"hp": 39, "ataque": 52, "defensa": 43, "ataque_especial": 60, "defensa_especial": 50, "velocidad": 65},
        "movimientos_posibles": [{"numero": 2, "nivel": 1}, {"numero": 3, "nivel": 1}, {"numero": 6, "nivel": 9}, {"numero": 7, "nivel": 15}],
        "evoluciona_a": 5, "nivel_evolucion": 16, "sprite": "sprite_ibermon_004",
        "catch_rate": 45, "exp_yield": 62, "growth_rate": "Medio",
    },
    {
        "numero": 5,  "nombre": "Charmeleon", "tipo1": "Fuego",   "tipo2": None,
        "descripcion": "Muy agresivo. Cuando siente un rival poderoso, la llama de su cola crece intensamente.",
        "stats_base": {"hp": 58, "ataque": 64, "defensa": 58, "ataque_especial": 80, "defensa_especial": 65, "velocidad": 80},
        "movimientos_posibles": [{"numero": 2, "nivel": 1}, {"numero": 6, "nivel": 1}, {"numero": 7, "nivel": 20}, {"numero": 8, "nivel": 30}],
        "evoluciona_a": 6, "nivel_evolucion": 36, "sprite": "sprite_ibermon_005",
        "catch_rate": 45, "exp_yield": 142, "growth_rate": "Medio",
    },
    {
        "numero": 6,  "nombre": "Charizard",  "tipo1": "Fuego",   "tipo2": "Volador",
        "descripcion": "Escupe fuego que derrite cualquier cosa. Vuela buscando rivales dignos de combatir.",
        "stats_base": {"hp": 78, "ataque": 84, "defensa": 78, "ataque_especial": 109, "defensa_especial": 85, "velocidad": 100},
        "movimientos_posibles": [{"numero": 2, "nivel": 1}, {"numero": 6, "nivel": 1}, {"numero": 8, "nivel": 1}, {"numero": 9, "nivel": 42}],
        "evoluciona_a": None, "nivel_evolucion": None, "sprite": "sprite_ibermon_006",
        "catch_rate": 45, "exp_yield": 240, "growth_rate": "Medio",
    },
    # ── Squirtle line ────────────────────────────────────────────────────────────
    {
        "numero": 7,  "nombre": "Squirtle",   "tipo1": "Agua",    "tipo2": None,
        "descripcion": "Cuando retrae su cuello en el caparazon, rocía agua con gran precision.",
        "stats_base": {"hp": 44, "ataque": 48, "defensa": 65, "ataque_especial": 50, "defensa_especial": 64, "velocidad": 43},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 4, "nivel": 1}, {"numero": 10, "nivel": 7}, {"numero": 11, "nivel": 13}],
        "evoluciona_a": 8, "nivel_evolucion": 16, "sprite": "sprite_ibermon_007",
        "catch_rate": 45, "exp_yield": 63, "growth_rate": "Medio",
    },
    {
        "numero": 8,  "nombre": "Wartortle",  "tipo1": "Agua",    "tipo2": None,
        "descripcion": "Su larga cola peluda indica longevidad. Puede esconder todo su cuerpo en el caparazon.",
        "stats_base": {"hp": 59, "ataque": 63, "defensa": 80, "ataque_especial": 65, "defensa_especial": 80, "velocidad": 58},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 10, "nivel": 1}, {"numero": 11, "nivel": 17}, {"numero": 13, "nivel": 28}],
        "evoluciona_a": 9, "nivel_evolucion": 36, "sprite": "sprite_ibermon_008",
        "catch_rate": 45, "exp_yield": 142, "growth_rate": "Medio",
    },
    {
        "numero": 9,  "nombre": "Blastoise",  "tipo1": "Agua",    "tipo2": None,
        "descripcion": "Los canones de agua de su caparazon disparan proyectiles con enorme precision.",
        "stats_base": {"hp": 79, "ataque": 83, "defensa": 100, "ataque_especial": 85, "defensa_especial": 105, "velocidad": 78},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 10, "nivel": 1}, {"numero": 13, "nivel": 1}, {"numero": 12, "nivel": 44}],
        "evoluciona_a": None, "nivel_evolucion": None, "sprite": "sprite_ibermon_009",
        "catch_rate": 45, "exp_yield": 239, "growth_rate": "Medio",
    },
    {
        "numero": 10, "nombre": "Chispon",   "tipo1": "Electrico", "tipo2": None,
        "descripcion": "Ibermon electrico comun. Sus mejillas almacenan electricidad.",
        "stats_base": {"hp": 35, "ataque": 55, "defensa": 40, "ataque_especial": 50, "defensa_especial": 50, "velocidad": 90},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 5, "nivel": 5}, {"numero": 18, "nivel": 9}, {"numero": 20, "nivel": 26}],
        "evoluciona_a": 11, "nivel_evolucion": 22, "sprite": "sprite_ibermon_010",
        "catch_rate": 190, "exp_yield": 82, "growth_rate": "Rapido",
    },
    {
        "numero": 11, "nombre": "Voltiger",  "tipo1": "Electrico", "tipo2": None,
        "descripcion": "Evolucion de Chispon. Genera electricidad al correr.",
        "stats_base": {"hp": 60, "ataque": 90, "defensa": 55, "ataque_especial": 90, "defensa_especial": 80, "velocidad": 110},
        "movimientos_posibles": [{"numero": 5, "nivel": 1}, {"numero": 18, "nivel": 1}, {"numero": 20, "nivel": 1}, {"numero": 19, "nivel": 44}],
        "evoluciona_a": None, "nivel_evolucion": None, "sprite": "sprite_ibermon_011",
        "catch_rate": 75, "exp_yield": 172, "growth_rate": "Rapido",
    },
    {
        "numero": 12, "nombre": "Gusanin",   "tipo1": "Bicho",    "tipo2": None,
        "descripcion": "Pequeno ibermon insecto. Muy debil pero facil de encontrar.",
        "stats_base": {"hp": 45, "ataque": 30, "defensa": 35, "ataque_especial": 20, "defensa_especial": 20, "velocidad": 45},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 2, "nivel": 1}, {"numero": 3, "nivel": 5}],
        "evoluciona_a": 13, "nivel_evolucion": 7, "sprite": "sprite_ibermon_012",
        "catch_rate": 255, "exp_yield": 39, "growth_rate": "Rapido",
    },
    {
        "numero": 13, "nombre": "Capuller",  "tipo1": "Bicho",    "tipo2": None,
        "descripcion": "Crisalida de Gusanin. Endurece su caparazon.",
        "stats_base": {"hp": 50, "ataque": 35, "defensa": 55, "ataque_especial": 25, "defensa_especial": 25, "velocidad": 30},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 4, "nivel": 1}],
        "evoluciona_a": 14, "nivel_evolucion": 10, "sprite": "sprite_ibermon_013",
        "catch_rate": 120, "exp_yield": 72, "growth_rate": "Rapido",
    },
    {
        "numero": 14, "nombre": "Mariphor",  "tipo1": "Bicho",    "tipo2": "Volador",
        "descripcion": "Forma final de Gusanin. Sus alas brillan con polvo magico.",
        "stats_base": {"hp": 60, "ataque": 45, "defensa": 50, "ataque_especial": 80, "defensa_especial": 80, "velocidad": 70},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 5, "nivel": 1}, {"numero": 15, "nivel": 12}, {"numero": 17, "nivel": 17}],
        "evoluciona_a": None, "nivel_evolucion": None, "sprite": "sprite_ibermon_014",
        "catch_rate": 45, "exp_yield": 178, "growth_rate": "Rapido",
    },
    {
        "numero": 15, "nombre": "Rocin",     "tipo1": "Roca",     "tipo2": None,
        "descripcion": "Ibermon de roca. Muy lento pero extremadamente resistente.",
        "stats_base": {"hp": 40, "ataque": 80, "defensa": 100, "ataque_especial": 30, "defensa_especial": 30, "velocidad": 20},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 3, "nivel": 1}, {"numero": 4, "nivel": 11}],
        "evoluciona_a": 16, "nivel_evolucion": 25, "sprite": "sprite_ibermon_015",
        "catch_rate": 255, "exp_yield": 58, "growth_rate": "Medio",
    },
    {
        "numero": 16, "nombre": "Petragon",  "tipo1": "Roca",     "tipo2": "Tierra",
        "descripcion": "Evolucion de Rocin. Su cuerpo es tan duro como el diamante.",
        "stats_base": {"hp": 80, "ataque": 120, "defensa": 130, "ataque_especial": 55, "defensa_especial": 65, "velocidad": 30},
        "movimientos_posibles": [{"numero": 1, "nivel": 1}, {"numero": 3, "nivel": 1}, {"numero": 4, "nivel": 1}, {"numero": 5, "nivel": 32}],
        "evoluciona_a": None, "nivel_evolucion": None, "sprite": "sprite_ibermon_016",
        "catch_rate": 45, "exp_yield": 171, "growth_rate": "Medio",
    },
]


# ──────────────────────────────────────────
# ITEMS
# ──────────────────────────────────────────
ITEMS = [
    {"numero": 1,  "nombre": "Pocion",        "descripcion": "Restaura 20 HP.",                          "tipo": "curacion", "efecto": {"tipo_efecto": "curacion_hp",    "valor": 20},            "precio": 300},
    {"numero": 2,  "nombre": "Super Pocion",  "descripcion": "Restaura 50 HP.",                          "tipo": "curacion", "efecto": {"tipo_efecto": "curacion_hp",    "valor": 50},            "precio": 700},
    {"numero": 3,  "nombre": "Hiper Pocion",  "descripcion": "Restaura 200 HP.",                         "tipo": "curacion", "efecto": {"tipo_efecto": "curacion_hp",    "valor": 200},           "precio": 1200},
    {"numero": 4,  "nombre": "Pocion Maxima", "descripcion": "Restaura todos los HP.",                   "tipo": "curacion", "efecto": {"tipo_efecto": "curacion_hp",    "valor": 9999},          "precio": 2500},
    {"numero": 5,  "nombre": "Antidoto",      "descripcion": "Cura el envenenamiento.",                  "tipo": "curacion", "efecto": {"tipo_efecto": "cura_veneno",    "valor": None},          "precio": 100},
    {"numero": 6,  "nombre": "Quemasal",      "descripcion": "Cura la quemadura.",                       "tipo": "curacion", "efecto": {"tipo_efecto": "cura_quemadura", "valor": None},          "precio": 250},
    {"numero": 7,  "nombre": "Paralyzer",     "descripcion": "Cura la paralisis.",                       "tipo": "curacion", "efecto": {"tipo_efecto": "cura_paralisis", "valor": None},          "precio": 200},
    {"numero": 8,  "nombre": "Revivir",       "descripcion": "Revive con la mitad de HP.",               "tipo": "curacion", "efecto": {"tipo_efecto": "revivir",        "valor": 0.5},           "precio": 1500},
    {"numero": 9,  "nombre": "Revivir Max",   "descripcion": "Revive con todos los HP.",                 "tipo": "curacion", "efecto": {"tipo_efecto": "revivir",        "valor": 1.0},           "precio": 4000},
    {"numero": 10, "nombre": "Iberball",      "descripcion": "Bola de captura basica.",                  "tipo": "captura",  "efecto": {"tipo_efecto": "captura",        "valor": 1.0},           "precio": 200},
    {"numero": 11, "nombre": "Super Ball",    "descripcion": "Mejor tasa de captura.",                   "tipo": "captura",  "efecto": {"tipo_efecto": "captura",        "valor": 1.5},           "precio": 600},
    {"numero": 12, "nombre": "Ultra Ball",    "descripcion": "Alta tasa de captura.",                    "tipo": "captura",  "efecto": {"tipo_efecto": "captura",        "valor": 2.0},           "precio": 1200},
    {"numero": 13, "nombre": "Master Ball",   "descripcion": "Captura cualquier ibermon sin fallo.",      "tipo": "captura",  "efecto": {"tipo_efecto": "captura",        "valor": 255},           "precio": 0},
    {"numero": 14, "nombre": "X Ataque",      "descripcion": "Sube el ataque en combate.",               "tipo": "batalla",  "efecto": {"tipo_efecto": "subir_ataque",   "valor": 1},             "precio": 500},
    {"numero": 15, "nombre": "X Defensa",     "descripcion": "Sube la defensa en combate.",              "tipo": "batalla",  "efecto": {"tipo_efecto": "subir_defensa",  "valor": 1},             "precio": 550},
    {"numero": 16, "nombre": "X Velocidad",   "descripcion": "Sube la velocidad en combate.",            "tipo": "batalla",  "efecto": {"tipo_efecto": "subir_velocidad","valor": 1},             "precio": 350},
    {"numero": 17, "nombre": "Mochila Vieja", "descripcion": "Una mochila abandonada. Abre una puerta.", "tipo": "clave",    "efecto": {"tipo_efecto": "clave",          "valor": "puerta_cueva_1"},"precio": 0},
    {"numero": 18, "nombre": "Llave del Gym", "descripcion": "Llave del gimnasio principal.",            "tipo": "clave",    "efecto": {"tipo_efecto": "clave",          "valor": "gym_1"},       "precio": 0},
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
# FUNCIONES DE SEED
# ──────────────────────────────────────────

async def seed_movimientos():
    count = await MovimientoCatalogo.count()
    if count > 0:
        print(f"  Ya hay {count} movimientos, omitiendo...")
        return
    await MovimientoCatalogo.insert_many([MovimientoCatalogo(**m) for m in MOVIMIENTOS])
    print(f"  {len(MOVIMIENTOS)} movimientos insertados")


async def seed_ibermon():
    count = await IbermonCatalogo.count()
    if count > 0:
        print(f"  Ya hay {count} ibermon, omitiendo...")
        return
    await IbermonCatalogo.insert_many([
        IbermonCatalogo(**{
            **ib,
            "stats_base": StatsBase(**ib["stats_base"]),
            "movimientos_posibles": [MovimientoPosible(**m) for m in ib["movimientos_posibles"]],
        })
        for ib in IBERMON
    ])
    print(f"  {len(IBERMON)} ibermon insertados")


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


async def main():
    print("Iniciando seed...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[IbermonCatalogo, MovimientoCatalogo, ItemCatalogo, LogroCatalogo],
    )
    await seed_movimientos()
    await seed_ibermon()
    await seed_items()
    await seed_logros()
    print("Seed completado")


if __name__ == "__main__":
    asyncio.run(main())
