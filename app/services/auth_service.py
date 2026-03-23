from fastapi import HTTPException, status

from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioRegistroSchema, UsuarioLoginSchema
from app.core.security import hash_password, verify_password, crear_token


async def registrar_usuario(datos: UsuarioRegistroSchema) -> Usuario:
    # Comprobar si el username ya existe
    username_existe = await Usuario.find_one(Usuario.username == datos.username)
    if username_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso",
        )

    # Comprobar si el email ya existe
    email_existe = await Usuario.find_one(Usuario.email == datos.email)
    if email_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está en uso",
        )

    nuevo_usuario = Usuario(
        username=datos.username,
        email=datos.email,
        hashed_password=hash_password(datos.password),
    )
    await nuevo_usuario.insert()
    return nuevo_usuario


async def login_usuario(datos: UsuarioLoginSchema) -> dict:
    usuario = await Usuario.find_one(Usuario.username == datos.username)
    if not usuario or not verify_password(datos.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    token = crear_token(data={"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}
