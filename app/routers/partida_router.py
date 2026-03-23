from fastapi import APIRouter, Depends

from app.schemas.partida_schema import (
    PartidaNuevaSchema,
    GuardarPartidaSchema,
    ActualizarPosicionSchema,
    PartidaResumenSchema,
    PartidaCompletaSchema,
)
from app.services import partida_service
from app.core.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/partidas", tags=["Partidas"])


@router.post("/", response_model=PartidaCompletaSchema, status_code=201)
async def nueva_partida(datos: PartidaNuevaSchema, usuario: Usuario = Depends(get_current_user)):
    return await partida_service.crear_partida(datos, usuario)


@router.get("/", response_model=list[PartidaResumenSchema])
async def listar_partidas(usuario: Usuario = Depends(get_current_user)):
    return await partida_service.obtener_partidas_usuario(usuario)


@router.get("/{partida_id}", response_model=PartidaCompletaSchema)
async def obtener_partida(partida_id: str, usuario: Usuario = Depends(get_current_user)):
    return await partida_service.obtener_partida_por_id(partida_id, usuario)


@router.put("/{partida_id}/guardar", response_model=PartidaCompletaSchema)
async def guardar_partida(partida_id: str, datos: GuardarPartidaSchema, usuario: Usuario = Depends(get_current_user)):
    return await partida_service.guardar_partida(partida_id, datos, usuario)


@router.patch("/{partida_id}/posicion")
async def actualizar_posicion(partida_id: str, datos: ActualizarPosicionSchema, usuario: Usuario = Depends(get_current_user)):
    return await partida_service.actualizar_posicion(partida_id, datos, usuario)
