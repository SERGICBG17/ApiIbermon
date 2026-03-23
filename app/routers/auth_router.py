from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.usuario_schema import UsuarioRegistroSchema, UsuarioPublicoSchema, TokenSchema
from app.services.auth_service import registrar_usuario, login_usuario
from app.core.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registro", response_model=UsuarioPublicoSchema, status_code=201)
async def registro(datos: UsuarioRegistroSchema):
    usuario = await registrar_usuario(datos)
    return UsuarioPublicoSchema(
        id=str(usuario.id),
        username=usuario.username,
        email=usuario.email,
        fecha_registro=usuario.fecha_registro,
        partidas=[str(p) for p in usuario.partidas],
    )


@router.post("/login", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    from app.schemas.usuario_schema import UsuarioLoginSchema
    datos = UsuarioLoginSchema(username=form_data.username, password=form_data.password)
    return await login_usuario(datos)


@router.get("/yo", response_model=UsuarioPublicoSchema)
async def yo(usuario: Usuario = Depends(get_current_user)):
    return UsuarioPublicoSchema(
        id=str(usuario.id),
        username=usuario.username,
        email=usuario.email,
        fecha_registro=usuario.fecha_registro,
        partidas=[str(p) for p in usuario.partidas],
    )
