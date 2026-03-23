from bson import ObjectId
from fastapi import HTTPException, status

from app.models.partida import Partida, Posicion
from app.models.usuario import Usuario
from app.schemas.partida_schema import (
    PartidaNuevaSchema,
    GuardarPartidaSchema,
    ActualizarPosicionSchema,
)


async def crear_partida(datos: PartidaNuevaSchema, usuario: Usuario) -> Partida:
    nueva_partida = Partida(
        usuario_id=usuario.id,
        personaje_elegido=datos.personaje_elegido,
        starter_elegido=datos.starter_elegido,
        mapa_actual="ciudad_inicial",
        posicion=Posicion(x=0, y=0),
    )
    await nueva_partida.insert()

    # Añadir la partida al array de partidas del usuario
    usuario.partidas.append(nueva_partida.id)
    await usuario.save()

    return nueva_partida


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
    partida.inventario = datos.inventario
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
    await partida.save()
    return partida
