from beanie import Document

class LogroCatalogo(Document):
    codigo: str                       # PK: "primer_combate", "captura_10", etc
    nombre: str
    descripcion: str
    condicion: str                    # descripcion de como se desbloquea
    icono: str                        # nombre del asset en Unity

    class Settings:
        name = "logro_catalogo"
