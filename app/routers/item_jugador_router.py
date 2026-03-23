from fastapi import APIRouter, Depends

from app.schemas.item_jugador_schema import (
    ItemJugadorAnadirSchema,
    ItemJugadorActualizarSchema,
    ItemJugadorSchema,
)
from app.services import item_jugador_service
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.item_jugador import ItemJugador


def item_to_schema(i: ItemJugador) -> ItemJugadorSchema:
    return ItemJugadorSchema(
        id=str(i.id),
        partida_id=str(i.partida_id),
        item_catalogo_id=i.item_catalogo_id,
        cantidad=i.cantidad,
    )


router = APIRouter(prefix="/partidas/{partida_id}/items", tags=["Items Jugador"])


@router.get("/")
async def ver_inventario(partida_id: str, usuario: Usuario = Depends(get_current_user)):
    items = await item_jugador_service.obtener_inventario(partida_id, usuario)
    return [item_to_schema(i) for i in items]


@router.post("/", status_code=201)
async def anadir_item(partida_id: str, datos: ItemJugadorAnadirSchema, usuario: Usuario = Depends(get_current_user)):
    item = await item_jugador_service.anadir_item(partida_id, datos, usuario)
    return item_to_schema(item)


@router.patch("/{item_id}")
async def actualizar_item(partida_id: str, item_id: str, datos: ItemJugadorActualizarSchema, usuario: Usuario = Depends(get_current_user)):
    item = await item_jugador_service.actualizar_item(partida_id, item_id, datos, usuario)
    return item_to_schema(item)


@router.delete("/{item_id}", status_code=204)
async def eliminar_item(partida_id: str, item_id: str, usuario: Usuario = Depends(get_current_user)):
    await item_jugador_service.eliminar_item(partida_id, item_id, usuario)
