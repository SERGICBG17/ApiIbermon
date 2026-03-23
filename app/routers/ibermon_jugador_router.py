from fastapi import APIRouter, Depends

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
