from fastapi import HTTPException, status

from app.models.item_jugador import ItemJugador
from app.models.usuario import Usuario
from app.schemas.item_jugador_schema import ItemJugadorAnadirSchema, ItemJugadorActualizarSchema
from app.services.partida_service import obtener_partida_por_id


async def obtener_inventario(partida_id: str, usuario: Usuario) -> list[ItemJugador]:
    partida = await obtener_partida_por_id(partida_id, usuario)
    return await ItemJugador.find(ItemJugador.partida_id == partida.id).to_list()


async def anadir_item(partida_id: str, datos: ItemJugadorAnadirSchema, usuario: Usuario) -> ItemJugador:
    partida = await obtener_partida_por_id(partida_id, usuario)

    # Si ya tiene ese item simplemente sumamos la cantidad
    item_existente = await ItemJugador.find_one(
        ItemJugador.partida_id == partida.id,
        ItemJugador.item_catalogo_id == datos.item_catalogo_id,
    )
    if item_existente:
        item_existente.cantidad += datos.cantidad
        await item_existente.save()
        return item_existente

    nuevo = ItemJugador(
        partida_id=partida.id,
        item_catalogo_id=datos.item_catalogo_id,
        cantidad=datos.cantidad,
    )
    await nuevo.insert()
    return nuevo


async def actualizar_item(partida_id: str, item_id: str, datos: ItemJugadorActualizarSchema, usuario: Usuario) -> ItemJugador:
    await obtener_partida_por_id(partida_id, usuario)

    item = await ItemJugador.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

    if datos.cantidad <= 0:
        # Si la cantidad llega a 0 o menos lo eliminamos directamente
        await item.delete()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    item.cantidad = datos.cantidad
    await item.save()
    return item


async def eliminar_item(partida_id: str, item_id: str, usuario: Usuario) -> None:
    await obtener_partida_por_id(partida_id, usuario)

    item = await ItemJugador.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

    await item.delete()
