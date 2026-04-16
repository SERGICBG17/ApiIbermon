from google import genai
from google.genai import types
from fastapi import HTTPException

from app.core.config import settings

SYSTEM_PROMPT = """Eres IberBot, el asistente oficial del videojuego Ibermon.

Ibermon es un RPG por turnos ambientado en la Península Ibérica, inspirado en Pokémon.
Los jugadores capturan criaturas llamadas Ibermon, las entrenan y combaten con ellas.

La web tiene estas secciones:
- Inicio: presentación del juego y vista previa del catálogo
- Catálogo: todos los Ibermon, movimientos, ítems y logros del juego
- Dashboard: las partidas guardadas del usuario (requiere haber iniciado sesión)
- Descarga: instrucciones para descargar el juego desde GitHub
- Login y Registro: para crear una cuenta o iniciar sesión

Tipos de Ibermon: Fuego, Agua, Planta, Eléctrico, Normal, Psíquico, Roca, Tierra,
Hielo, Siniestro, Volador, Veneno, Dragón, Acero, Bicho, Lucha y Fantasma.

Sistema de combate:
- Los combates son por turnos, como en Pokémon
- Cada Ibermon tiene 6 estadísticas base: HP, Ataque, Defensa, Ataque Especial, Defensa Especial y Velocidad
- Cada Ibermon puede aprender hasta 4 movimientos
- Los movimientos tienen tres categorías: Físico, Especial y Estado
- Los jugadores pueden tener un equipo de hasta 6 Ibermon activos y el resto en el centro Ibermon

Responde siempre en español. Sé amable, conciso y usa algún emoji ocasionalmente.
Si alguien pregunta por datos muy específicos de un Ibermon o movimiento (stats exactos, etc.),
dirígelo al Catálogo de la web donde puede consultarlos en detalle."""


def _get_client() -> genai.Client:
    if not settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY.strip():
        raise HTTPException(
            status_code=503,
            detail="El chatbot no está configurado. Añade GEMINI_API_KEY al .env.",
        )
    return genai.Client(api_key=settings.GEMINI_API_KEY.strip())


async def responder(mensaje: str) -> str:
    client = _get_client()
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=mensaje,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )
        return response.text
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error al contactar con Gemini: {e}")
