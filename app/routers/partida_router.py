from fastapi import APIRouter, Depends

from app.schemas.partida_schema import (
    PartidaNuevaSchema,
    GuardarPartidaSchema,
    ActualizarPosicionSchema,
    PartidaResumenSchema,
    PartidaCompletaSchema,
    PosicionSchema,
    ItemInventarioSchema,
)
from app.services import partida_service
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.models.partida import Partida


def partida_to_completa(p: Partida) -> PartidaCompletaSchema:
    return PartidaCompletaSchema(
        id=str(p.id),
        usuario_id=str(p.usuario_id),
        personaje_elegido=p.personaje_elegido,
        starter_elegido=p.starter_elegido,
        mapa_actual=p.mapa_actual,
        posicion=PosicionSchema(x=p.posicion.x, y=p.posicion.y),
        dinero=p.dinero,
        tiempo_jugado=p.tiempo_jugado,
        equipo=[str(e) for e in p.equipo],
        centro_ibermon=[str(c) for c in p.centro_ibermon],
        inventario=[
            ItemInventarioSchema(item_catalogo_id=i.item_catalogo_id, cantidad=i.cantidad)
            for i in p.inventario
        ],
        pokedex_visto=p.pokedex_visto,
        pokedex_capturado=p.pokedex_capturado,
        medallas=p.medallas,
        logros=p.logros,
        combates_ganados=p.combates_ganados,
        combates_perdidos=p.combates_perdidos,
        flags=p.flags,
    )


def partida_to_resumen(p: Partida) -> PartidaResumenSchema:
    return PartidaResumenSchema(
        id=str(p.id),
        personaje_elegido=p.personaje_elegido,
        mapa_actual=p.mapa_actual,
        tiempo_jugado=p.tiempo_jugado,
        medallas=p.medallas,
        combates_ganados=p.combates_ganados,
        combates_perdidos=p.combates_perdidos,
    )


router = APIRouter(prefix="/partidas", tags=["Partidas"])


@router.post("/", status_code=201)
async def nueva_partida(datos: PartidaNuevaSchema, usuario: Usuario = Depends(get_current_user)):
    partida = await partida_service.crear_partida(datos, usuario)
    return partida_to_completa(partida)


@router.get("/")
async def listar_partidas(usuario: Usuario = Depends(get_current_user)):
    partidas = await partida_service.obtener_partidas_usuario(usuario)
    return [partida_to_resumen(p) for p in partidas]


@router.get("/{partida_id}")
async def obtener_partida(partida_id: str, usuario: Usuario = Depends(get_current_user)):
    partida = await partida_service.obtener_partida_por_id(partida_id, usuario)
    return partida_to_completa(partida)


@router.put("/{partida_id}/guardar")
async def guardar_partida(partida_id: str, datos: GuardarPartidaSchema, usuario: Usuario = Depends(get_current_user)):
    partida = await partida_service.guardar_partida(partida_id, datos, usuario)
    return partida_to_completa(partida)


@router.patch("/{partida_id}/posicion")
async def actualizar_posicion(partida_id: str, datos: ActualizarPosicionSchema, usuario: Usuario = Depends(get_current_user)):
    partida = await partida_service.actualizar_posicion(partida_id, datos, usuario)
    return partida_to_completa(partida)
