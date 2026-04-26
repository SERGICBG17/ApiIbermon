from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.partida.partida import Partida, Posicion
from app.models.usuario import Usuario
from app.models.ibermon_jugador.ibermon_jugador import IbermonJugador, MovimientoAprendido
from app.models.item_jugador import ItemJugador
from app.models.ibermon_catalogo.ibermon_catalogo import IbermonCatalogo
from app.models.movimiento_catalogo import MovimientoCatalogo
from app.schemas.partida.partida_schema import (
    PartidaNuevaSchema,
    GuardarPartidaSchema,
    ActualizarPosicionSchema,
)

_NIVEL_STARTER = 5


async def crear_partida(datos: PartidaNuevaSchema, usuario: Usuario) -> Partida:
    nueva_partida = Partida(
        usuario_id=usuario.id,
        nombre=datos.nombre,
        personaje_elegido=datos.personaje_elegido,
        mapa_actual="CasaPersonaje",
        posicion=Posicion(x=7.008884, y=6.872112),
        fecha_creacion=datos.fecha_creacion or datetime.now(timezone.utc),
        ultima_conexion=datetime.now(timezone.utc),
    )
    await nueva_partida.insert()

    usuario.partidas.append(nueva_partida.id)
    await usuario.save()
    return nueva_partida


async def elegir_starter(partida_id: str, starter_numero: int, usuario: Usuario) -> Partida:
    partida = await obtener_partida_por_id(partida_id, usuario)

    if partida.starter_elegido is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya tienes un starter")

    catalogo = await IbermonCatalogo.find_one(IbermonCatalogo.numero == starter_numero)
    if not catalogo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Starter no encontrado")

    movs_disponibles = sorted(
        [m for m in catalogo.movimientos_posibles if m.nivel <= _NIVEL_STARTER],
        key=lambda m: m.nivel,
    )[-4:]

    movimientos = []
    for mp in movs_disponibles:
        mov_cat = await MovimientoCatalogo.find_one(MovimientoCatalogo.numero == mp.numero)
        if mov_cat:
            movimientos.append(MovimientoAprendido(numero=mp.numero, pp=mov_cat.pp))

    hp_inicial = (catalogo.stats_base.hp * _NIVEL_STARTER // 50) + _NIVEL_STARTER + 10

    starter = IbermonJugador(
        partida_id=partida.id,
        ibermon_catalogo_id=starter_numero,
        nivel=_NIVEL_STARTER,
        hp_actual=hp_inicial,
        ubicacion="equipo",
        movimientos_aprendidos=movimientos,
    )
    await starter.insert()

    partida.starter_elegido = starter_numero
    partida.equipo.append(starter.id)
    await partida.save()
    return partida


async def obtener_partidas_usuario(usuario: Usuario) -> list[Partida]:
    return await Partida.find(Partida.usuario_id == usuario.id).to_list()


async def obtener_partida_por_id(partida_id: str, usuario: Usuario) -> Partida:
    partida = await Partida.get(partida_id)
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida no encontrada")
    if partida.usuario_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes acceso a esta partida")
    return partida


async def guardar_partida(partida_id: str, datos: GuardarPartidaSchema, usuario: Usuario) -> Partida:
    partida = await obtener_partida_por_id(partida_id, usuario)

    partida.mapa_actual = datos.mapa_actual
    partida.posicion = Posicion(x=datos.posicion.x, y=datos.posicion.y)
    partida.dinero = datos.dinero
    partida.tiempo_jugado = datos.tiempo_jugado
    partida.pokedex_visto = datos.pokedex_visto
    partida.pokedex_capturado = datos.pokedex_capturado
    partida.medallas = datos.medallas
    partida.logros = datos.logros
    partida.combates_ganados = datos.combates_ganados
    partida.combates_perdidos = datos.combates_perdidos
    partida.flags = datos.flags

    await partida.save()
    return partida


async def actualizar_posicion(partida_id: str, datos: ActualizarPosicionSchema, usuario: Usuario) -> Partida:
    partida = await obtener_partida_por_id(partida_id, usuario)
    partida.mapa_actual = datos.mapa_actual
    partida.posicion = Posicion(x=datos.posicion.x, y=datos.posicion.y)
    partida.tiempo_jugado = datos.tiempo_jugado
    partida.ultima_conexion = datos.ultima_conexion or datetime.now(timezone.utc)
    await partida.save()
    return partida


async def eliminar_partida(partida_id: str, usuario: Usuario) -> None:
    partida = await obtener_partida_por_id(partida_id, usuario)

    await IbermonJugador.find(IbermonJugador.partida_id == partida.id).delete()
    await ItemJugador.find(ItemJugador.partida_id == partida.id).delete()

    usuario.partidas = [p for p in usuario.partidas if p != partida.id]
    await usuario.save()

    await partida.delete()
