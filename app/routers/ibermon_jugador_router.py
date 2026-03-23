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

router = APIRouter(prefix="/partidas/{partida_id}/ibermon", tags=["Ibermon Jugador"])


@router.get("/equipo", response_model=list[IbermonJugadorSchema])
async def ver_equipo(partida_id: str, usuario: Usuario = Depends(get_current_user)):
    return await ibermon_jugador_service.obtener_equipo(partida_id, usuario)


@router.get("/centro", response_model=list[IbermonJugadorSchema])
async def ver_centro(partida_id: str, usuario: Usuario = Depends(get_current_user)):
    return await ibermon_jugador_service.obtener_centro(partida_id, usuario)


@router.post("/", response_model=IbermonJugadorSchema, status_code=201)
async def anadir_ibermon(partida_id: str, datos: IbermonJugadorCrearSchema, usuario: Usuario = Depends(get_current_user)):
    return await ibermon_jugador_service.anadir_ibermon(partida_id, datos, usuario)


@router.patch("/{ibermon_id}/mover", response_model=IbermonJugadorSchema)
async def mover_ibermon(partida_id: str, ibermon_id: str, datos: IbermonJugadorMoverSchema, usuario: Usuario = Depends(get_current_user)):
    return await ibermon_jugador_service.mover_ibermon(partida_id, ibermon_id, datos, usuario)


@router.patch("/{ibermon_id}", response_model=IbermonJugadorSchema)
async def actualizar_ibermon(partida_id: str, ibermon_id: str, datos: IbermonJugadorActualizarSchema, usuario: Usuario = Depends(get_current_user)):
    return await ibermon_jugador_service.actualizar_ibermon(ibermon_id, datos, usuario)
