from fastapi import APIRouter

from app.services import catalogo_service
from app.schemas.ibermon_catalogo.ibermon_catalogo_schema import IbermonCatalogoResumenSchema, IbermonCatalogoDetalleSchema
from app.schemas.movimiento_catalogo_schema import MovimientoCatalogoResumenSchema, MovimientoCatalogoDetalleSchema
from app.schemas.item_catalogo.item_catalogo_schema import ItemCatalogoResumenSchema, ItemCatalogoDetalleSchema, ItemCatalogoCrearSchema
from app.schemas.logro_schema import LogroCatalogoSchema
from app.schemas.entrenador_catalogo.entrenador_catalogo_schema import (
    EntrenadorCatalogoResumenSchema,
    EntrenadorCatalogoDetalleSchema,
    EntrenadorCatalogoCrearSchema,
)

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

@router.post("/items", response_model=ItemCatalogoDetalleSchema, status_code=201)
async def crear_item(datos: ItemCatalogoCrearSchema):
    """Crea un item nuevo en el catalogo. Falla si ya existe uno con el mismo numero."""
    return await catalogo_service.crear_item(datos)


@router.post("/items/bulk", status_code=201)
async def crear_items_bulk(datos: list[ItemCatalogoCrearSchema]):
    """Crea varios items de golpe en el catalogo. Salta los que ya existian."""
    return await catalogo_service.crear_items_bulk(datos)

# --- LOGROS ---

@router.get("/logros", response_model=list[LogroCatalogoSchema])
async def listar_logros():
    return await catalogo_service.obtener_todos_logros()


@router.get("/logros/{codigo}", response_model=LogroCatalogoSchema)
async def detalle_logro(codigo: str):
    return await catalogo_service.obtener_logro_por_codigo(codigo)


# --- ENTRENADORES ---

@router.get("/entrenadores", response_model=list[EntrenadorCatalogoResumenSchema])
async def listar_entrenadores():
    return await catalogo_service.obtener_todos_entrenadores()


@router.get("/entrenadores/{numero}", response_model=EntrenadorCatalogoDetalleSchema)
async def detalle_entrenador(numero: int):
    return await catalogo_service.obtener_entrenador_por_numero(numero)


@router.get("/entrenadores/por-nombre/{nombre}", response_model=EntrenadorCatalogoDetalleSchema)
async def detalle_entrenador_por_nombre(nombre: str):
    return await catalogo_service.obtener_entrenador_por_nombre(nombre)


@router.post("/entrenadores", response_model=EntrenadorCatalogoDetalleSchema, status_code=201)
async def crear_entrenador(datos: EntrenadorCatalogoCrearSchema):
    return await catalogo_service.crear_entrenador(datos)


@router.post("/entrenadores/bulk", status_code=201)
async def crear_entrenadores_bulk(datos: list[EntrenadorCatalogoCrearSchema]):
    return await catalogo_service.crear_entrenadores_bulk(datos)
