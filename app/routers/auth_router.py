from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.usuario_schema import UsuarioRegistroSchema, UsuarioPublicoSchema, TokenSchema
from app.services.auth_service import registrar_usuario, login_usuario
from app.core.security import get_current_user
from app.models.usuario import Usuario


def usuario_to_publico(u: Usuario) -> UsuarioPublicoSchema:
    return UsuarioPublicoSchema(
        id=str(u.id),
        username=u.username,
        email=u.email,
        fecha_registro=u.fecha_registro,
        partidas=[str(p) for p in u.partidas],
    )


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registro", status_code=201)
async def registro(datos: UsuarioRegistroSchema):
    usuario = await registrar_usuario(datos)
    return usuario_to_publico(usuario)


@router.post("/login", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    from app.schemas.usuario_schema import UsuarioLoginSchema
    datos = UsuarioLoginSchema(username=form_data.username, password=form_data.password)
    return await login_usuario(datos)


@router.get("/yo")
async def yo(usuario: Usuario = Depends(get_current_user)):
    return usuario_to_publico(usuario)
