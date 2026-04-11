from fastapi import HTTPException, status

from app.models.ibermon_jugador import IbermonJugador, MovimientoAprendido
from app.models.usuario import Usuario
from app.schemas.ibermon_jugador_schema import (
    IbermonJugadorCrearSchema,
    IbermonJugadorMoverSchema,
    IbermonJugadorActualizarSchema,
)
from app.services.partida_service import obtener_partida_por_id


async def obtener_ibermon_o_404(ibermon_id: str) -> IbermonJugador:
    ibermon = await IbermonJugador.get(ibermon_id)
    if not ibermon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ibermon no encontrado")
    return ibermon


async def anadir_ibermon(partida_id: str, datos: IbermonJugadorCrearSchema, usuario: Usuario) -> IbermonJugador:
    partida = await obtener_partida_por_id(partida_id, usuario)

    if datos.ubicacion == "equipo" and len(partida.equipo) >= 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El equipo ya tiene 6 ibermon. Mueve uno al centro primero",
        )

    nuevo = IbermonJugador(
        partida_id=partida.id,
        ibermon_catalogo_id=datos.ibermon_catalogo_id,
        nickname=datos.nickname,
        nivel=datos.nivel,
        hp_actual=datos.hp_actual,
        ubicacion=datos.ubicacion,
    )
    await nuevo.insert()

    if datos.ubicacion == "equipo":
        partida.equipo.append(nuevo.id)
    else:
        partida.centro_ibermon.append(nuevo.id)

    await partida.save()
    return nuevo


async def mover_ibermon(partida_id: str, ibermon_id: str, datos: IbermonJugadorMoverSchema, usuario: Usuario) -> IbermonJugador:
    partida = await obtener_partida_por_id(partida_id, usuario)
    ibermon = await obtener_ibermon_o_404(ibermon_id)

    if datos.ubicacion == "equipo" and len(partida.equipo) >= 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El equipo ya tiene 6 ibermon",
        )

    if ibermon.ubicacion == "equipo":
        partida.equipo.remove(ibermon.id)
        partida.centro_ibermon.append(ibermon.id)
    else:
        partida.centro_ibermon.remove(ibermon.id)
        partida.equipo.append(ibermon.id)

    ibermon.ubicacion = datos.ubicacion
    await ibermon.save()
    await partida.save()
    return ibermon


async def actualizar_ibermon(ibermon_id: str, datos: IbermonJugadorActualizarSchema, usuario: Usuario) -> IbermonJugador:
    ibermon = await obtener_ibermon_o_404(ibermon_id)

    if datos.nivel is not None:
        ibermon.nivel = datos.nivel
    if datos.experiencia is not None:
        ibermon.experiencia = datos.experiencia
    if datos.hp_actual is not None:
        ibermon.hp_actual = datos.hp_actual
    if datos.movimientos_aprendidos is not None:
        if len(datos.movimientos_aprendidos) > 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un ibermon solo puede tener 4 movimientos",
            )
        ibermon.movimientos_aprendidos = [
            MovimientoAprendido(numero=m.numero, pp=m.pp)
            for m in datos.movimientos_aprendidos
        ]
    if datos.nickname is not None:
        ibermon.nickname = datos.nickname

    await ibermon.save()
    return ibermon


async def eliminar_ibermon(partida_id: str, ibermon_id: str, usuario: Usuario) -> None:
    partida = await obtener_partida_por_id(partida_id, usuario)
    ibermon = await obtener_ibermon_o_404(ibermon_id)

    # Quitarlo de la lista correspondiente en la partida
    if ibermon.ubicacion == "equipo":
        partida.equipo = [e for e in partida.equipo if e != ibermon.id]
    else:
        partida.centro_ibermon = [c for c in partida.centro_ibermon if c != ibermon.id]

    await partida.save()
    await ibermon.delete()


async def obtener_equipo(partida_id: str, usuario: Usuario) -> list[IbermonJugador]:
    partida = await obtener_partida_por_id(partida_id, usuario)
    return await IbermonJugador.find(
        IbermonJugador.partida_id == partida.id,
        IbermonJugador.ubicacion == "equipo"
    ).to_list()


async def obtener_centro(partida_id: str, usuario: Usuario) -> list[IbermonJugador]:
    partida = await obtener_partida_por_id(partida_id, usuario)
    return await IbermonJugador.find(
        IbermonJugador.partida_id == partida.id,
        IbermonJugador.ubicacion == "centro"
    ).to_list()
