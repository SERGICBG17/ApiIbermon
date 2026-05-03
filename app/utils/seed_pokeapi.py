"""
app/utils/seed_pokeapi.py
═══════════════════════════════════════════════════════════════════════════════
Pobla la base de datos con los 649 Pokémon de la era Black & White (Gen 1–5)
usando datos en tiempo real de PokéAPI (https://pokeapi.co).

Datos que se importan
─────────────────────
  • Nombre en español (o inglés como fallback)
  • Tipos traducidos al español
  • Estadísticas base (HP, ATK, DEF, SP.ATK, SP.DEF, VEL)
  • Descripción del Pokédex en español
  • Movimientos aprendidos por subida de nivel en Black/White
  • Cadena de evolución (a quién evoluciona y a qué nivel)
  • Sprite animado Gen V (BW animated GIF) o el mejor disponible
  • Catch rate, EXP yield y curva de crecimiento

Uso
───
  python -m app.utils.seed_pokeapi                      # #1–649
  python -m app.utils.seed_pokeapi --desde 494          # solo Gen 5
  python -m app.utils.seed_pokeapi --desde 1 --hasta 9  # solo los primeros
  python -m app.utils.seed_pokeapi --force              # borra y re-inserta todo

Requisitos extra
────────────────
  pip install httpx
  (o:  pip install -r requirements.txt)
═══════════════════════════════════════════════════════════════════════════════
"""

import asyncio
import argparse
import sys
import time
from typing import Dict, List, Optional, Set, Tuple

import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.ibermon_catalogo import IbermonCatalogo, StatsBase, MovimientoPosible
from app.models.movimiento_catalogo import MovimientoCatalogo


# ── Parámetros globales ───────────────────────────────────────────────────────

POKEAPI_BASE   = "https://pokeapi.co/api/v2"
MAX_CONCURRENT = 20        # peticiones simultáneas máximas (sé amable con la API)
HTTP_TIMEOUT   = 40.0      # segundos por petición
RETRY_MAX      = 4         # reintentos ante error de red
INSERT_BATCH   = 100       # tamaño del batch para insertar en MongoDB

# Version groups de Black & White (prioridad alta)
BW_GROUPS = {"black-white", "black-2-white-2"}

# Version groups adicionales como fallback de moveset
FALLBACK_GROUPS = {
    "heartgold-soulsilver", "platinum", "diamond-pearl",
    "firered-leafgreen", "emerald", "ruby-sapphire",
    "crystal", "gold-silver", "yellow", "red-blue",
}

# ── Mapas de traducción ───────────────────────────────────────────────────────

TYPE_MAP: Dict[str, str] = {
    "normal":    "Normal",    "fire":     "Fuego",
    "water":     "Agua",      "grass":    "Planta",
    "electric":  "Eléctrico", "ice":      "Hielo",
    "fighting":  "Lucha",     "poison":   "Veneno",
    "ground":    "Tierra",    "flying":   "Volador",
    "psychic":   "Psíquico",  "bug":      "Bicho",
    "rock":      "Roca",      "ghost":    "Fantasma",
    "dragon":    "Dragón",    "dark":     "Siniestro",
    "steel":     "Acero",     "fairy":    "Hada",
}

GROWTH_MAP: Dict[str, str] = {
    "slow":                "Lento",
    "medium":              "Medio",
    "fast":                "Rápido",
    "medium-slow":         "Medio-Lento",
    "slow-then-very-fast": "Errático",
    "fast-then-very-slow": "Fluctuante",
}

CATEGORY_MAP: Dict[str, str] = {
    "physical": "Fisico",    # sin acento → coincide con el modelo
    "special":  "Especial",
    "status":   "Estado",
}

# Targets que significan "afecta al propio usuario"
TARGET_SELF = {
    "user", "user-and-allies", "users-field",
    "entire-field", "ally", "all-allies",
}


# ══════════════════════════════════════════════════════════════════════════════
#  HTTP
# ══════════════════════════════════════════════════════════════════════════════

async def fetch(
    client: httpx.AsyncClient,
    sem:    asyncio.Semaphore,
    url:    str,
) -> Optional[dict]:
    """Descarga JSON con reintentos exponenciales. Devuelve None si 404 o error."""
    for attempt in range(RETRY_MAX):
        try:
            async with sem:
                r = await client.get(url, timeout=HTTP_TIMEOUT)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            if attempt < RETRY_MAX - 1:
                await asyncio.sleep(1.5 ** attempt)
        except httpx.HTTPError:
            if attempt < RETRY_MAX - 1:
                await asyncio.sleep(1.5 ** attempt)
    return None


# ══════════════════════════════════════════════════════════════════════════════
#  UTILIDADES DE PARSEO
# ══════════════════════════════════════════════════════════════════════════════

def _localized(entries: list, field: str, langs: tuple = ("es", "en")) -> str:
    """Devuelve el texto del primer idioma preferido que encuentre."""
    by_lang: Dict[str, str] = {}
    for e in entries:
        lang = e.get("language", {}).get("name", "")
        text = e.get(field, "").replace("\n", " ").replace("\f", " ").strip()
        if text and lang in langs and lang not in by_lang:
            by_lang[lang] = text
    for lang in langs:
        if lang in by_lang:
            return by_lang[lang]
    # Último recurso: cualquier texto disponible
    for e in entries:
        text = e.get(field, "").replace("\n", " ").replace("\f", " ").strip()
        if text:
            return text
    return ""


def pokemon_name(species: dict) -> str:
    return _localized(species.get("names", []), "name") or ""


def pokemon_desc(species: dict) -> str:
    return _localized(species.get("flavor_text_entries", []), "flavor_text") or "Sin descripción."


def move_name(move: dict) -> str:
    return _localized(move.get("names", []), "name") or move.get("name", "").capitalize()


def move_desc(move: dict) -> str:
    return _localized(move.get("flavor_text_entries", []), "flavor_text") or "Sin descripción."


def move_short_effect(move: dict) -> Optional[str]:
    text = _localized(move.get("effect_entries", []), "short_effect")
    # Reemplazar marcador de efecto chance
    if text:
        chance = move.get("effect_chance") or 0
        text = text.replace("$effect_chance", str(chance))
    return text or None


def get_sprite_frontal(pokemon: dict) -> str:
    """
    Prioridad de sprite frontal:
      1. Gen V BW animated front_default (.gif)
      2. Gen V BW static front_default (.png)
      3. Official artwork front_default
      4. sprites.front_default (fallback)
    """
    try:
        bw = pokemon["sprites"]["versions"]["generation-v"]["black-white"]
        anim = (bw.get("animated") or {}).get("front_default")
        if anim:
            return anim
        static = bw.get("front_default")
        if static:
            return static
    except (KeyError, TypeError):
        pass
    try:
        art = pokemon["sprites"]["other"]["official-artwork"]["front_default"]
        if art:
            return art
    except (KeyError, TypeError):
        pass
    return pokemon.get("sprites", {}).get("front_default") or ""


def get_sprite_trasero(pokemon: dict) -> str:
    """
    Prioridad de sprite trasero:
      1. Gen V BW animated back_default (.gif)
      2. Gen V BW static back_default (.png)
      3. sprites.back_default (fallback)
    """
    try:
        bw = pokemon["sprites"]["versions"]["generation-v"]["black-white"]
        anim = (bw.get("animated") or {}).get("back_default")
        if anim:
            return anim
        static = bw.get("back_default")
        if static:
            return static
    except (KeyError, TypeError):
        pass
    return pokemon.get("sprites", {}).get("back_default") or ""


def get_level_up_moves(pokemon: dict) -> List[Tuple[int, int]]:
    """
    Devuelve [(move_id, level)] aprendidos por subida de nivel.
    Prioriza moveset de BW; si no hay, coge cualquier version group.
    """
    bw_moves:  Dict[int, int] = {}
    all_moves: Dict[int, int] = {}

    for entry in pokemon.get("moves", []):
        move_id = int(entry["move"]["url"].rstrip("/").split("/")[-1])
        for vgd in entry.get("version_group_details", []):
            if vgd["move_learn_method"]["name"] != "level-up":
                continue
            level = vgd.get("level_learned_at", 0)
            vg    = vgd["version_group"]["name"]

            # Guardar el nivel mínimo en el que se aprende
            if vg in BW_GROUPS:
                if move_id not in bw_moves or level < bw_moves[move_id]:
                    bw_moves[move_id] = level
            if move_id not in all_moves or level < all_moves[move_id]:
                all_moves[move_id] = level

    chosen = bw_moves if bw_moves else all_moves
    return sorted(chosen.items(), key=lambda x: x[1])  # ordenados por nivel


def parse_chain(node: dict, evo_map: Dict[int, Tuple[int, Optional[int]]]):
    """Rellena evo_map: {from_id: (to_id, min_level_or_None)}."""
    from_id = int(node["species"]["url"].rstrip("/").split("/")[-1])
    for evo in node.get("evolves_to", []):
        to_id = int(evo["species"]["url"].rstrip("/").split("/")[-1])
        min_level: Optional[int] = None
        for detail in evo.get("evolution_details", []):
            if detail.get("trigger", {}).get("name") == "level-up":
                min_level = detail.get("min_level")
                break
        evo_map[from_id] = (to_id, min_level)
        parse_chain(evo, evo_map)


# ══════════════════════════════════════════════════════════════════════════════
#  CONSTRUCTORES DE DOCUMENTOS
# ══════════════════════════════════════════════════════════════════════════════

def build_move_doc(move_id: int, data: dict) -> Optional[MovimientoCatalogo]:
    try:
        tipo      = TYPE_MAP.get(data["type"]["name"], data["type"]["name"].capitalize())
        categoria = CATEGORY_MAP.get(
            (data.get("damage_class") or {}).get("name", "status"), "Estado"
        )
        target    = (data.get("target") or {}).get("name", "")
        objetivo  = "Self" if target in TARGET_SELF else "Foe"

        return MovimientoCatalogo(
            numero         = move_id,
            nombre         = move_name(data) or f"Move-{move_id}",
            tipo           = tipo,
            potencia       = data.get("power")    or 0,
            precision      = data.get("accuracy") or 0,
            pp             = data.get("pp")        or 1,
            descripcion    = move_desc(data),
            efecto         = move_short_effect(data),
            categoria      = categoria,
            objetivo       = objetivo,
            siempre_acierta= data.get("accuracy") is None,
            prioridad      = data.get("priority") or 0,
        )
    except Exception as e:
        print(f"\n  ⚠ Movimiento {move_id}: {e}")
        return None


def build_ibermon_doc(
    num:             int,
    pokemon:         dict,
    species:         dict,
    evo_map:         Dict[int, Tuple[int, Optional[int]]],
    available_moves: Set[int],
) -> Optional[IbermonCatalogo]:
    try:
        # Nombre
        nombre = pokemon_name(species) or pokemon.get("name", f"Ibermon{num}").capitalize()

        # Tipos
        types = sorted(pokemon["types"], key=lambda t: t["slot"])
        tipo1 = TYPE_MAP.get(types[0]["type"]["name"], types[0]["type"]["name"].capitalize())
        tipo2 = (
            TYPE_MAP.get(types[1]["type"]["name"], types[1]["type"]["name"].capitalize())
            if len(types) > 1 else None
        )

        # Stats
        raw = {s["stat"]["name"]: s["base_stat"] for s in pokemon.get("stats", [])}
        stats = StatsBase(
            hp               = raw.get("hp",              1),
            ataque           = raw.get("attack",           1),
            defensa          = raw.get("defense",          1),
            ataque_especial  = raw.get("special-attack",   1),
            defensa_especial = raw.get("special-defense",  1),
            velocidad        = raw.get("speed",            1),
        )

        # Movimientos aprendibles por nivel (solo los que existen en BD)
        movs = [
            MovimientoPosible(numero=mid, nivel=nivel)
            for mid, nivel in get_level_up_moves(pokemon)
            if mid in available_moves
        ]

        # Evolución
        evoluciona_a    = None
        nivel_evolucion = None
        if num in evo_map:
            to_id, lvl = evo_map[num]
            if 1 <= to_id <= 649:
                evoluciona_a    = to_id
                nivel_evolucion = lvl

        return IbermonCatalogo(
            numero           = num,
            nombre           = nombre,
            tipo1            = tipo1,
            tipo2            = tipo2,
            descripcion      = pokemon_desc(species),
            stats_base       = stats,
            movimientos_posibles = movs,
            evoluciona_a     = evoluciona_a,
            nivel_evolucion  = nivel_evolucion,
            sprite_frontal   = get_sprite_frontal(pokemon),
            sprite_trasero   = get_sprite_trasero(pokemon),
            catch_rate       = species.get("capture_rate",      255),
            exp_yield        = pokemon.get("base_experience") or 100,
            growth_rate      = GROWTH_MAP.get(
                (species.get("growth_rate") or {}).get("name", "medium"), "Medio"
            ),
        )
    except Exception as e:
        print(f"\n  ⚠ Pokémon #{num}: {e}")
        return None


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

async def main(start: int, end: int, force: bool):
    t0 = time.time()
    width = 56
    sep   = "═" * width

    print(f"\n{sep}")
    print(f"  Ibermon Seed — PokéAPI  Black & White  (#{start}–#{end})")
    print(sep)

    # ── Conexión DB ───────────────────────────────────────────────────────────
    print("\n► Conectando a MongoDB...")
    db_client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=db_client[settings.MONGO_DB_NAME],
        document_models=[IbermonCatalogo, MovimientoCatalogo],
    )
    print("  ✓ Conectado")

    # ── Force: vaciar colecciones ─────────────────────────────────────────────
    if force:
        print("  ⚠  --force: vaciando colecciones existentes...")
        await IbermonCatalogo.find_all().delete()
        await MovimientoCatalogo.find_all().delete()
        print("  ✓ Colecciones vaciadas")
    else:
        n_ib  = await IbermonCatalogo.count()
        n_mov = await MovimientoCatalogo.count()
        if n_ib > 0 or n_mov > 0:
            print(f"\n  Ya existen datos en BD ({n_ib} ibermon, {n_mov} movimientos).")
            print("  Usa --force para sobreescribir. Abortando.\n")
            return

    nums = list(range(start, end + 1))
    sem  = asyncio.Semaphore(MAX_CONCURRENT)

    async with httpx.AsyncClient(
        base_url=POKEAPI_BASE,
        headers={"User-Agent": "IbermonSeed/1.0"},
        timeout=HTTP_TIMEOUT,
    ) as http:

        # ══ FASE 1: Pokémon + Especies ════════════════════════════════════════
        print(f"\n► Fase 1/3 — Descargando {len(nums)} Pokémon + Especies...")

        async def fetch_pair(n: int):
            poke    = await fetch(http, sem, f"/pokemon/{n}")
            species = await fetch(http, sem, f"/pokemon-species/{n}")
            return n, poke, species

        raw_pairs = await asyncio.gather(*[fetch_pair(n) for n in nums])
        valid = [(n, p, s) for n, p, s in raw_pairs if p and s]

        if not valid:
            print("  ✗ No se pudo descargar ningún Pokémon. Comprueba tu conexión.")
            return

        n_ok    = len(valid)
        n_fail  = len(nums) - n_ok
        fail_str = f"  ({n_fail} fallaron)" if n_fail else ""
        print(f"  ✓ {n_ok}/{len(nums)} Pokémon obtenidos{fail_str}")

        # ══ FASE 2: Cadenas Evolutivas ════════════════════════════════════════
        print("\n► Fase 2/3 — Cadenas evolutivas...")
        chain_urls: Set[str] = set()
        for _, _, species in valid:
            url = (species.get("evolution_chain") or {}).get("url")
            if url:
                chain_urls.add(url)

        chain_results = await asyncio.gather(
            *[fetch(http, sem, url) for url in chain_urls]
        )
        evo_map: Dict[int, Tuple[int, Optional[int]]] = {}
        for chain in chain_results:
            if chain and "chain" in chain:
                parse_chain(chain["chain"], evo_map)

        print(f"  ✓ {len(chain_urls)} cadenas → {len(evo_map)} evoluciones mapeadas")

        # ══ FASE 3: Movimientos ═══════════════════════════════════════════════
        print("\n► Fase 3/3 — Movimientos de nivel (Black & White)...")

        all_move_ids: Set[int] = set()
        for _, pokemon, _ in valid:
            for mid, _ in get_level_up_moves(pokemon):
                all_move_ids.add(mid)

        print(f"  Movimientos únicos encontrados: {len(all_move_ids)}")
        print(f"  Descargando detalles...")

        move_raw = await asyncio.gather(
            *[fetch(http, sem, f"/move/{mid}") for mid in sorted(all_move_ids)]
        )

        move_docs: List[MovimientoCatalogo] = []
        for mid, data in zip(sorted(all_move_ids), move_raw):
            if data:
                doc = build_move_doc(mid, data)
                if doc:
                    move_docs.append(doc)

        if move_docs:
            for i in range(0, len(move_docs), INSERT_BATCH):
                await MovimientoCatalogo.insert_many(move_docs[i:i + INSERT_BATCH])
            print(f"  ✓ {len(move_docs)} movimientos insertados en BD")
        else:
            print("  ⚠ No se insertaron movimientos")

        available_moves: Set[int] = {m.numero for m in move_docs}

        # ══ CONSTRUIR E INSERTAR IBERMON ══════════════════════════════════════
        print(f"\n► Construyendo {n_ok} Ibermon...")

        ibermon_docs: List[IbermonCatalogo] = []
        for i, (num, pokemon, species) in enumerate(valid, 1):
            doc = build_ibermon_doc(num, pokemon, species, evo_map, available_moves)
            if doc:
                ibermon_docs.append(doc)

            # Barra de progreso
            pct    = i / n_ok
            filled = int(pct * 30)
            bar    = "█" * filled + "░" * (30 - filled)
            name   = (pokemon.get("name") or "?").capitalize()[:14].ljust(14)
            print(f"  [{bar}] {i:>3}/{n_ok}  #{num:>3} {name}", end="\r", flush=True)

        print()  # nueva línea

        print(f"  Insertando en MongoDB...")
        for i in range(0, len(ibermon_docs), INSERT_BATCH):
            await IbermonCatalogo.insert_many(ibermon_docs[i:i + INSERT_BATCH])

        print(f"  ✓ {len(ibermon_docs)} Ibermon insertados en BD")

    # ── Resumen final ─────────────────────────────────────────────────────────
    elapsed      = time.time() - t0
    mins, secs   = divmod(int(elapsed), 60)

    print(f"\n{sep}")
    print(f"  ✓  Seed completado en {mins}m {secs}s")
    print(f"     Ibermon insertados  : {len(ibermon_docs)}")
    print(f"     Movimientos         : {len(move_docs)}")
    print(f"     Evoluciones mapeadas: {len(evo_map)}")
    print(sep)
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Puebla la BD de Ibermon con los 649 Pokémon de la era Black & White.\n"
            "Usa PokéAPI para obtener nombres en español, sprites BW animados, "
            "estadísticas, movimientos y cadenas evolutivas."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--desde", type=int, default=1,
        help="Número de Pokémon desde el que empezar (default: 1)",
    )
    parser.add_argument(
        "--hasta", type=int, default=649,
        help="Número de Pokémon hasta el que llegar (default: 649)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Borra los datos existentes antes de insertar (DESTRUCTIVO)",
    )
    args = parser.parse_args()

    if not (1 <= args.desde <= args.hasta <= 649):
        print("Error: --desde y --hasta deben estar entre 1 y 649, y desde ≤ hasta.")
        sys.exit(1)

    asyncio.run(main(args.desde, args.hasta, args.force))
