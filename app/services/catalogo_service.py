from fastapi import HTTPException, status

from app.models.ibermon_catalogo.ibermon_catalogo import IbermonCatalogo
from app.models.movimiento_catalogo import MovimientoCatalogo
from app.models.item_catalogo.item_catalogo import ItemCatalogo
from app.models.logro_catalogo import LogroCatalogo
from app.models.item_catalogo.efecto_item import EfectoItem
from app.models.entrenador_catalogo import EntrenadorCatalogo, EquipoEntrenador, DialogosEntrenador
from app.schemas.item_catalogo.item_catalogo_schema import ItemCatalogoCrearSchema
from app.schemas.entrenador_catalogo.entrenador_catalogo_schema import EntrenadorCatalogoCrearSchema

# --- IBERMON CATALOGO ---

async def obtener_todos_ibermon() -> list[IbermonCatalogo]:
    return await IbermonCatalogo.find_all().to_list()


async def obtener_ibermon_por_numero(numero: int) -> IbermonCatalogo:
    ibermon = await IbermonCatalogo.find_one(IbermonCatalogo.numero == numero)
    if not ibermon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ibermon no encontrado")
    return ibermon


# --- MOVIMIENTO CATALOGO ---

async def obtener_todos_movimientos() -> list[MovimientoCatalogo]:
    return await MovimientoCatalogo.find_all().to_list()


async def obtener_movimiento_por_numero(numero: int) -> MovimientoCatalogo:
    movimiento = await MovimientoCatalogo.find_one(MovimientoCatalogo.numero == numero)
    if not movimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movimiento no encontrado")
    return movimiento


# --- ITEM CATALOGO ---

async def obtener_todos_items() -> list[ItemCatalogo]:
    return await ItemCatalogo.find_all().to_list()


async def obtener_item_por_numero(numero: int) -> ItemCatalogo:
    item = await ItemCatalogo.find_one(ItemCatalogo.numero == numero)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    return item
async def crear_item(datos: ItemCatalogoCrearSchema) -> ItemCatalogo:
    """Crea un item nuevo en el catalogo."""
    existente = await ItemCatalogo.find_one(ItemCatalogo.numero == datos.numero)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un item con numero={datos.numero}",
        )

    nuevo = ItemCatalogo(
        numero=datos.numero,
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        tipo=datos.tipo,
        efecto=EfectoItem(
            tipo_efecto=datos.efecto.tipo_efecto,
            valor=datos.efecto.valor,
        ),
        precio=datos.precio,
    )
    await nuevo.insert() # type: ignore
    return nuevo


async def crear_items_bulk(datos: list[ItemCatalogoCrearSchema]) -> dict:
    """Inserta varios items de golpe en el catalogo. Los duplicados se saltan."""
    creados = []
    ya_existian = []

    for item_data in datos:
        existente = await ItemCatalogo.find_one(ItemCatalogo.numero == item_data.numero)
        if existente:
            ya_existian.append(item_data.numero)
            continue

        nuevo = ItemCatalogo(
            numero=item_data.numero,
            nombre=item_data.nombre,
            descripcion=item_data.descripcion,
            tipo=item_data.tipo,
            efecto=EfectoItem(
                tipo_efecto=item_data.efecto.tipo_efecto,
                valor=item_data.efecto.valor,
            ),
            precio=item_data.precio,
        )
        await nuevo.insert()  # type: ignore
        creados.append(item_data.numero)

    return {
        "creados": creados,
        "ya_existian": ya_existian,
        "total_creados": len(creados),
    }


# --- LOGRO CATALOGO ---

async def obtener_todos_logros() -> list[LogroCatalogo]:
    return await LogroCatalogo.find_all().to_list()


async def obtener_logro_por_codigo(codigo: str) -> LogroCatalogo:
    logro = await LogroCatalogo.find_one(LogroCatalogo.codigo == codigo)
    if not logro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logro no encontrado")
    return logro


# --- ENTRENADOR CATALOGO ---

async def obtener_todos_entrenadores() -> list[EntrenadorCatalogo]:
    return await EntrenadorCatalogo.find_all().to_list()


async def obtener_entrenador_por_numero(numero: int) -> EntrenadorCatalogo:
    entrenador = await EntrenadorCatalogo.find_one(EntrenadorCatalogo.numero == numero)
    if not entrenador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrenador no encontrado")
    return entrenador


async def obtener_entrenador_por_nombre(nombre: str) -> EntrenadorCatalogo:
    entrenador = await EntrenadorCatalogo.find_one(EntrenadorCatalogo.nombre == nombre)
    if not entrenador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrenador no encontrado")
    return entrenador


async def crear_entrenador(datos: EntrenadorCatalogoCrearSchema) -> EntrenadorCatalogo:
    """Crea un entrenador nuevo en el catalogo."""
    existente = await EntrenadorCatalogo.find_one(EntrenadorCatalogo.numero == datos.numero)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un entrenador con numero={datos.numero}",
        )

    nuevo = EntrenadorCatalogo(
        numero=datos.numero,
        nombre=datos.nombre,
        equipo=[EquipoEntrenador(**e.model_dump()) for e in datos.equipo],
        recompensa=datos.recompensa,
        dialogos=DialogosEntrenador(**datos.dialogos.model_dump()),
        sprite=datos.sprite,
    )
    await nuevo.insert()  # type: ignore
    return nuevo


async def crear_entrenadores_bulk(datos: list[EntrenadorCatalogoCrearSchema]) -> dict:
    """Inserta varios entrenadores de golpe. Los duplicados se saltan."""
    creados = []
    ya_existian = []

    for ent in datos:
        existente = await EntrenadorCatalogo.find_one(EntrenadorCatalogo.numero == ent.numero)
        if existente:
            ya_existian.append(ent.numero)
            continue

        nuevo = EntrenadorCatalogo(
            numero=ent.numero,
            nombre=ent.nombre,
            equipo=[EquipoEntrenador(**e.model_dump()) for e in ent.equipo],
            recompensa=ent.recompensa,
            dialogos=DialogosEntrenador(**ent.dialogos.model_dump()),
            sprite=ent.sprite,
        )
        await nuevo.insert()  # type: ignore
        creados.append(ent.numero)

    return {
        "creados": creados,
        "ya_existian": ya_existian,
        "total_creados": len(creados),
    }
