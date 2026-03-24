from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.ibermon_jugador_schema import (
    IbermonJugadorCrearSchema,
    IbermonJugadorMoverSchema,
    IbermonJugadorActualizarSchema,
    IbermonJugadorSchema,
)
from app.services import ibermon_jugador_service
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.ibermon_jugador import IbermonJugador


def ibermon_to_schema(ib: IbermonJugador) -> IbermonJugadorSchema:
    return IbermonJugadorSchema(
        id=str(ib.id),
        partida_id=str(ib.partida_id),
        ibermon_catalogo_id=ib.ibermon_catalogo_id,
        nickname=ib.nickname,
        nivel=ib.nivel,
        experiencia=ib.experiencia,
        hp_actual=ib.hp_actual,
        ubicacion=ib.ubicacion,
        movimientos_aprendidos=ib.movimientos_aprendidos,
    )


router = APIRouter(prefix="/partidas/{partida_id}/ibermon", tags=["Ibermon Jugador"])


@router.get("/equipo")
async def ver_equipo(partida_id: str, usuario: Usuario = Depends(get_current_user)):
    ibermons = await ibermon_jugador_service.obtener_equipo(partida_id, usuario)
    return [ibermon_to_schema(ib) for ib in ibermons]


@router.get("/centro")
async def ver_centro(partida_id: str, usuario: Usuario = Depends(get_current_user)):
    ibermons = await ibermon_jugador_service.obtener_centro(partida_id, usuario)
    return [ibermon_to_schema(ib) for ib in ibermons]


@router.post("/", status_code=201)
async def anadir_ibermon(partida_id: str, datos: IbermonJugadorCrearSchema, usuario: Usuario = Depends(get_current_user)):
    ibermon = await ibermon_jugador_service.anadir_ibermon(partida_id, datos, usuario)
    return ibermon_to_schema(ibermon)


@router.patch("/{ibermon_id}/mover")
async def mover_ibermon(partida_id: str, ibermon_id: str, datos: IbermonJugadorMoverSchema, usuario: Usuario = Depends(get_current_user)):
    ibermon = await ibermon_jugador_service.mover_ibermon(partida_id, ibermon_id, datos, usuario)
    return ibermon_to_schema(ibermon)


@router.patch("/{ibermon_id}")
async def actualizar_ibermon(partida_id: str, ibermon_id: str, datos: IbermonJugadorActualizarSchema, usuario: Usuario = Depends(get_current_user)):
    ibermon = await ibermon_jugador_service.actualizar_ibermon(ibermon_id, datos, usuario)
    return ibermon_to_schema(ibermon)


@router.delete("/{ibermon_id}", status_code=204)
async def eliminar_ibermon(partida_id: str, ibermon_id: str, usuario: Usuario = Depends(get_current_user)):
    await ibermon_jugador_service.eliminar_ibermon(partida_id, ibermon_id, usuario)


# --- MOVIMIENTOS DEL IBERMON ---

@router.put("/{ibermon_id}/movimientos")
async def actualizar_movimientos(
    partida_id: str,
    ibermon_id: str,
    movimientos: list[int],
    usuario: Usuario = Depends(get_current_user)
):
    """
    Actualiza los movimientos aprendidos de un ibermon.
    Recibe una lista de numeros de movimiento (ref MovimientoCatalogo).
    Maximo 4 movimientos.
    """
    if len(movimientos) > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un ibermon solo puede tener 4 movimientos"
        )
    ibermon = await ibermon_jugador_service.obtener_ibermon_o_404(ibermon_id)
    ibermon.movimientos_aprendidos = movimientos
    await ibermon.save()
    return ibermon_to_schema(ibermon)


@router.post("/{ibermon_id}/movimientos/{numero_movimiento}", status_code=201)
async def aprender_movimiento(
    partida_id: str,
    ibermon_id: str,
    numero_movimiento: int,
    usuario: Usuario = Depends(get_current_user)
):
    """Añade un movimiento al ibermon. Maximo 4."""
    ibermon = await ibermon_jugador_service.obtener_ibermon_o_404(ibermon_id)

    if numero_movimiento in ibermon.movimientos_aprendidos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ibermon ya tiene ese movimiento"
        )
    if len(ibermon.movimientos_aprendidos) >= 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ibermon ya tiene 4 movimientos. Elimina uno primero"
        )

    ibermon.movimientos_aprendidos.append(numero_movimiento)
    await ibermon.save()
    return ibermon_to_schema(ibermon)


@router.delete("/{ibermon_id}/movimientos/{numero_movimiento}", status_code=204)
async def olvidar_movimiento(
    partida_id: str,
    ibermon_id: str,
    numero_movimiento: int,
    usuario: Usuario = Depends(get_current_user)
):
    """Elimina un movimiento del ibermon."""
    ibermon = await ibermon_jugador_service.obtener_ibermon_o_404(ibermon_id)

    if numero_movimiento not in ibermon.movimientos_aprendidos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ibermon no tiene ese movimiento"
        )

    ibermon.movimientos_aprendidos.remove(numero_movimiento)
    await ibermon.save()
