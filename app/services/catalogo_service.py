from fastapi import HTTPException, status

from app.models.ibermon_catalogo import IbermonCatalogo
from app.models.movimiento_catalogo import MovimientoCatalogo
from app.models.item_catalogo import ItemCatalogo
from app.models.logro_catalogo import LogroCatalogo


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


# --- LOGRO CATALOGO ---

async def obtener_todos_logros() -> list[LogroCatalogo]:
    return await LogroCatalogo.find_all().to_list()


async def obtener_logro_por_codigo(codigo: str) -> LogroCatalogo:
    logro = await LogroCatalogo.find_one(LogroCatalogo.codigo == codigo)
    if not logro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logro no encontrado")
    return logro
