from fastapi import APIRouter

from app.services import catalogo_service
from app.schemas.ibermon_catalogo_schema import IbermonCatalogoResumenSchema, IbermonCatalogoDetalleSchema
from app.schemas.movimiento_catalogo_schema import MovimientoCatalogoResumenSchema, MovimientoCatalogoDetalleSchema
from app.schemas.item_catalogo_schema import ItemCatalogoResumenSchema, ItemCatalogoDetalleSchema
from app.schemas.logro_schema import LogroCatalogoSchema

router = APIRouter(prefix="/catalogo", tags=["Catálogos Públicos"])


# --- IBERMON ---

@router.get("/ibermon", response_model=list[IbermonCatalogoResumenSchema])
async def listar_ibermon():
    return await catalogo_service.obtener_todos_ibermon()


@router.get("/ibermon/{numero}", response_model=IbermonCatalogoDetalleSchema)
async def detalle_ibermon(numero: int):
    return await catalogo_service.obtener_ibermon_por_numero(numero)


# --- MOVIMIENTOS ---

@router.get("/movimientos", response_model=list[MovimientoCatalogoResumenSchema])
async def listar_movimientos():
    return await catalogo_service.obtener_todos_movimientos()


@router.get("/movimientos/{numero}", response_model=MovimientoCatalogoDetalleSchema)
async def detalle_movimiento(numero: int):
    return await catalogo_service.obtener_movimiento_por_numero(numero)


# --- ITEMS ---

@router.get("/items", response_model=list[ItemCatalogoResumenSchema])
async def listar_items():
    return await catalogo_service.obtener_todos_items()


@router.get("/items/{numero}", response_model=ItemCatalogoDetalleSchema)
async def detalle_item(numero: int):
    return await catalogo_service.obtener_item_por_numero(numero)


# --- LOGROS ---

@router.get("/logros", response_model=list[LogroCatalogoSchema])
async def listar_logros():
    return await catalogo_service.obtener_todos_logros()


@router.get("/logros/{codigo}", response_model=LogroCatalogoSchema)
async def detalle_logro(codigo: str):
    return await catalogo_service.obtener_logro_por_codigo(codigo)
