# ApiIbermon

API REST del videojuego **Ibermon**, un RPG 2D tipo Pokémon ambientado en la Península Ibérica. Construida con FastAPI y MongoDB. Gestiona autenticación de usuarios, partidas guardadas, equipos de Ibermon, inventario y catálogos públicos.

---

## Índice

1. [Stack tecnológico](#stack-tecnológico)
2. [Estructura del proyecto](#estructura-del-proyecto)
3. [Modelos de datos](#modelos-de-datos)
4. [Endpoints](#endpoints)
   - [Auth](#auth)
   - [Partidas](#partidas)
   - [Ibermon del jugador](#ibermon-del-jugador)
   - [Ítems del jugador](#ítems-del-jugador)
   - [Catálogos públicos](#catálogos-públicos)
5. [Autenticación JWT](#autenticación-jwt)
6. [Configuración CORS](#configuración-cors)
7. [Variables de entorno](#variables-de-entorno)
8. [Puesta en marcha](#puesta-en-marcha)
   - [Local con uvicorn](#local-con-uvicorn)
   - [Con Docker](#con-docker)
9. [Scripts de seed](#scripts-de-seed)
   - [seed.py — Datos base del juego](#seedpy--datos-base-del-juego)
   - [seed_pokeapi.py — Pokémon Black & White](#seed_pokeapipy--pokémon-black--white)
   - [clean.py — Borrar catálogos](#cleanpy--borrar-catálogos)

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Framework web | FastAPI |
| Servidor ASGI | Uvicorn |
| Base de datos | MongoDB 7.0 |
| ODM | Beanie (sobre Motor) |
| Autenticación | JWT (python-jose) + bcrypt |
| Validación | Pydantic v2 |
| HTTP cliente (seed) | httpx |
| Contenedores | Docker + Docker Compose |

---

## Estructura del proyecto

```
ApiIbermon/
│
├── app/
│   ├── main.py              # Punto de entrada: FastAPI app + CORS + routers
│   │
│   ├── core/
│   │   ├── config.py        # Settings (Pydantic BaseSettings, lee .env)
│   │   └── security.py      # JWT: crear token, get_current_user dependency
│   │
│   ├── db/
│   │   └── session.py       # connect_db(): inicia Beanie con todos los modelos
│   │
│   ├── models/              # Documentos Beanie (colecciones MongoDB)
│   │   ├── usuario.py           # Colección: usuarios
│   │   ├── partida.py           # Colección: partidas
│   │   ├── ibermon_jugador.py   # Colección: ibermon_jugador
│   │   ├── item_jugador.py      # Colección: item_jugador
│   │   ├── ibermon_catalogo.py  # Colección: ibermon_catalogo
│   │   ├── movimiento_catalogo.py # Colección: movimiento_catalogo
│   │   ├── item_catalogo.py     # Colección: item_catalogo
│   │   └── logro_catalogo.py    # Colección: logro_catalogo
│   │
│   ├── schemas/             # Pydantic schemas (request/response)
│   │   ├── usuario_schema.py
│   │   ├── partida_schema.py
│   │   ├── ibermon_jugador_schema.py
│   │   ├── item_jugador_schema.py
│   │   ├── ibermon_catalogo_schema.py
│   │   ├── movimiento_catalogo_schema.py
│   │   ├── item_catalogo_schema.py
│   │   └── logro_schema.py
│   │
│   ├── routers/             # Rutas FastAPI
│   │   ├── auth_router.py
│   │   ├── partida_router.py
│   │   ├── ibermon_jugador_router.py
│   │   ├── item_jugador_router.py
│   │   └── catalogo_router.py
│   │
│   ├── services/            # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── partida_service.py
│   │   ├── ibermon_jugador_service.py
│   │   ├── item_jugador_service.py
│   │   └── catalogo_service.py
│   │
│   └── utils/               # Scripts de utilidad
│       ├── seed.py              # Seed manual: datos base del juego
│       ├── seed_pokeapi.py      # Seed automático: 649 Pokémon de B&W via PokéAPI
│       └── clean.py             # Borra colecciones de catálogo
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env                     # Variables de entorno (NO subir a git)
```

---

## Modelos de datos

### `Usuario`
**Colección:** `usuarios`

| Campo | Tipo | Descripción |
|---|---|---|
| `username` | `str` | Nombre de usuario único |
| `email` | `EmailStr` | Email único |
| `hashed_password` | `str` | Contraseña hasheada con bcrypt |
| `fecha_registro` | `datetime` | Fecha de alta (auto) |
| `partidas` | `List[ObjectId]` | Referencias a partidas del usuario |

---

### `Partida`
**Colección:** `partidas`

| Campo | Tipo | Descripción |
|---|---|---|
| `usuario_id` | `ObjectId` | Referencia al usuario propietario |
| `personaje_elegido` | `str` | Nombre del personaje (sprite) |
| `starter_elegido` | `int` | Número de Ibermon inicial en el catálogo |
| `mapa_actual` | `str` | Nombre de la escena Unity actual |
| `posicion` | `Posicion(x,y)` | Coordenadas en el mapa actual |
| `dinero` | `int` | Monedas del jugador |
| `tiempo_jugado` | `int` | Segundos totales jugados |
| `equipo` | `List[ObjectId]` | Hasta 6 IbermonJugador activos |
| `centro_ibermon` | `List[ObjectId]` | IbermonJugador en el centro |
| `pokedex_visto` | `List[int]` | Números de ibermon vistos |
| `pokedex_capturado` | `List[int]` | Números de ibermon capturados |
| `medallas` | `List[str]` | Medallas de gimnasio obtenidas |
| `logros` | `List[str]` | Códigos de logros desbloqueados |
| `combates_ganados` | `int` | Total de combates ganados |
| `combates_perdidos` | `int` | Total de combates perdidos |
| `flags` | `Dict[str,bool]` | Flags de progreso del mundo |

---

### `IbermonJugador`
**Colección:** `ibermon_jugador`

| Campo | Tipo | Descripción |
|---|---|---|
| `partida_id` | `ObjectId` | Partida a la que pertenece |
| `ibermon_catalogo_id` | `int` | Número en el catálogo (ej: 25 = Pikachu) |
| `nickname` | `str?` | Apodo personalizado (opcional) |
| `nivel` | `int` | Nivel actual (1–100) |
| `experiencia` | `int` | Puntos de experiencia acumulados |
| `hp_actual` | `int` | HP restantes (0 = debilitado) |
| `ubicacion` | `str` | `"equipo"` o `"centro"` |
| `movimientos_aprendidos` | `List[{numero, pp}]` | Hasta 4 movimientos con PP actuales |

---

### `ItemJugador`
**Colección:** `item_jugador`

| Campo | Tipo | Descripción |
|---|---|---|
| `partida_id` | `ObjectId` | Partida propietaria |
| `item_catalogo_id` | `int` | Número del ítem en catálogo |
| `cantidad` | `int` | Unidades en el inventario |

---

### `IbermonCatalogo`
**Colección:** `ibermon_catalogo`

| Campo | Tipo | Descripción |
|---|---|---|
| `numero` | `int` | PK (ej: 1=Bulbasaur, 25=Pikachu) |
| `nombre` | `str` | Nombre en español |
| `tipo1` | `str` | Tipo primario en español |
| `tipo2` | `str?` | Tipo secundario (opcional) |
| `descripcion` | `str` | Texto del Pokédex en español |
| `stats_base` | `StatsBase` | HP, ATK, DEF, SP.ATK, SP.DEF, VEL |
| `movimientos_posibles` | `List[{numero,nivel}]` | Movimientos aprendibles por nivel |
| `evoluciona_a` | `int?` | Número del ibermon al que evoluciona |
| `nivel_evolucion` | `int?` | Nivel mínimo para evolucionar (null = piedra/otro) |
| `sprite` | `str` | URL del sprite (GIF animado BW o PNG) |
| `catch_rate` | `int` | Tasa de captura 0–255 |
| `exp_yield` | `int` | EXP base al derrotar |
| `growth_rate` | `str` | Curva de crecimiento |

---

### `MovimientoCatalogo`
**Colección:** `movimiento_catalogo`

| Campo | Tipo | Descripción |
|---|---|---|
| `numero` | `int` | PK |
| `nombre` | `str` | Nombre en español |
| `tipo` | `str` | Tipo en español |
| `potencia` | `int` | Daño base (0 = movimiento de estado) |
| `precision` | `int` | Precisión 0–100 (0 = siempre acierta o estado) |
| `pp` | `int` | Usos máximos |
| `descripcion` | `str` | Descripción del movimiento |
| `efecto` | `str?` | Efecto secundario (quemadura, parálisis…) |
| `categoria` | `str` | `"Fisico"` / `"Especial"` / `"Estado"` |
| `objetivo` | `str` | `"Foe"` (enemigo) / `"Self"` (usuario) |
| `siempre_acierta` | `bool` | Si ignora el chequeo de precisión |
| `prioridad` | `int` | Orden de turno (+1 va antes, -1 va después) |

> **Nota:** `categoria` usa `"Fisico"` sin tilde para consistencia con el modelo.

---

### `ItemCatalogo`
**Colección:** `item_catalogo`

| Campo | Tipo | Descripción |
|---|---|---|
| `numero` | `int` | PK |
| `nombre` | `str` | Nombre del ítem |
| `descripcion` | `str` | Descripción |
| `tipo` | `str` | `"curacion"` / `"captura"` / `"batalla"` / `"clave"` |
| `efecto` | `EfectoItem` | `{tipo_efecto, valor}` |
| `precio` | `int` | Precio en tienda (0 = no vendible) |

---

### `LogroCatalogo`
**Colección:** `logro_catalogo`

| Campo | Tipo | Descripción |
|---|---|---|
| `codigo` | `str` | PK (ej: `"primer_combate"`) |
| `nombre` | `str` | Nombre visible del logro |
| `descripcion` | `str` | Descripción del logro |
| `condicion` | `str` | Descripción de cómo se desbloquea |
| `icono` | `str` | Nombre del asset en Unity |

---

## Endpoints

### Auth
**Prefijo:** `/auth` | **Tag:** `Auth`

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `POST` | `/auth/registro` | No | Registra un nuevo usuario |
| `POST` | `/auth/login` | No | Login → devuelve JWT |
| `GET`  | `/auth/yo` | JWT | Datos del usuario autenticado |

**`POST /auth/registro`**
```json
// Body
{ "username": "ash", "email": "ash@ibermon.es", "password": "secreto123" }

// Response 201
{ "id": "...", "username": "ash", "email": "ash@ibermon.es", "fecha_registro": "...", "partidas": [] }
```

**`POST /auth/login`**
```
// Body: form-data (application/x-www-form-urlencoded)
username=ash&password=secreto123

// Response 200
{ "access_token": "eyJ...", "token_type": "bearer" }
```

**`GET /auth/yo`**
```
// Header: Authorization: Bearer eyJ...

// Response 200
{ "id": "...", "username": "ash", "email": "ash@ibermon.es", "fecha_registro": "...", "partidas": ["..."] }
```

---

### Partidas
**Prefijo:** `/partidas` | **Tag:** `Partidas` | **Auth:** JWT requerido

| Método | Ruta | Descripción |
|---|---|---|
| `POST`  | `/partidas/` | Crear nueva partida |
| `GET`   | `/partidas/` | Listar partidas del usuario (resumen) |
| `GET`   | `/partidas/{id}` | Detalle completo de una partida |
| `PUT`   | `/partidas/{id}/guardar` | Guardar estado completo del juego |
| `PATCH` | `/partidas/{id}/posicion` | Actualizar solo posición y mapa |
| `DELETE`| `/partidas/{id}` | Eliminar partida |

**`POST /partidas/`**
```json
// Body
{ "personaje_elegido": "Alba", "starter_elegido": 4 }

// Response 201 — PartidaCompletaSchema
```

**`PUT /partidas/{id}/guardar`**
```json
// Body
{
  "mapa_actual": "Pueblo_Paleta",
  "posicion": { "x": 12.5, "y": 8.0 },
  "dinero": 500,
  "tiempo_jugado": 3600,
  "pokedex_visto": [1, 4, 7],
  "pokedex_capturado": [4],
  "medallas": ["Medalla_Roca"],
  "logros": ["primer_combate"],
  "combates_ganados": 5,
  "combates_perdidos": 1,
  "flags": { "intro_completada": true, "gym1_derrotado": true }
}
```

---

### Ibermon del jugador
**Prefijo:** `/partidas/{partida_id}/ibermon` | **Tag:** `Ibermon Jugador` | **Auth:** JWT

| Método | Ruta | Descripción |
|---|---|---|
| `GET`    | `…/equipo` | Ver los ibermon en el equipo activo |
| `GET`    | `…/centro` | Ver los ibermon en el centro |
| `POST`   | `…/` | Añadir un ibermon capturado a la partida |
| `PATCH`  | `…/{ibermon_id}/mover` | Mover entre equipo y centro |
| `PATCH`  | `…/{ibermon_id}` | Actualizar stats (nivel, HP, EXP…) |
| `DELETE` | `…/{ibermon_id}` | Eliminar ibermon |
| `PUT`    | `…/{ibermon_id}/movimientos` | Reemplazar los 4 movimientos |
| `POST`   | `…/{ibermon_id}/movimientos/{num}` | Aprender un movimiento nuevo |
| `DELETE` | `…/{ibermon_id}/movimientos/{num}` | Olvidar un movimiento |

> Un ibermon puede tener **máximo 4 movimientos** simultáneos.

---

### Ítems del jugador
**Prefijo:** `/partidas/{partida_id}/items` | **Tag:** `Items Jugador` | **Auth:** JWT

| Método | Ruta | Descripción |
|---|---|---|
| `GET`    | `…/` | Ver inventario completo |
| `POST`   | `…/` | Añadir ítem al inventario |
| `PATCH`  | `…/{item_id}` | Actualizar cantidad |
| `DELETE` | `…/{item_id}` | Eliminar ítem |

---

### Catálogos públicos
**Prefijo:** `/catalogo` | **Tag:** `Catálogos Públicos` | **Auth:** No requerida

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/catalogo/ibermon` | Lista todos los ibermon (resumen) |
| `GET` | `/catalogo/ibermon/{numero}` | Detalle completo de un ibermon |
| `GET` | `/catalogo/movimientos` | Lista todos los movimientos |
| `GET` | `/catalogo/movimientos/{numero}` | Detalle de un movimiento |
| `GET` | `/catalogo/items` | Lista todos los ítems |
| `GET` | `/catalogo/items/{numero}` | Detalle de un ítem |
| `GET` | `/catalogo/logros` | Lista todos los logros |
| `GET` | `/catalogo/logros/{codigo}` | Detalle de un logro |

---

## Autenticación JWT

El flujo completo de autenticación:

```
1. POST /auth/login  →  { access_token: "eyJ..." }
2. Todas las rutas protegidas requieren el header:
       Authorization: Bearer eyJ...
3. La dependency get_current_user() decodifica el JWT y
   devuelve el objeto Usuario de la BD.
4. Si el token es inválido o ha expirado → 401 Unauthorized
```

**Configuración del token:**
```
Algoritmo : HS256
Expiración: 60 minutos (configurable en .env)
Clave     : SECRET_KEY (definida en .env)
```

---

## Configuración CORS

El middleware de CORS está configurado en `app/main.py` para permitir peticiones desde el frontend web:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Docker frontend / servidor local
        "http://localhost:5500",    # VS Code Live Server
        "http://127.0.0.1:5500",
        "http://localhost:5501",
        "http://127.0.0.1:5501",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Si el frontend corre en otro puerto, añádelo a la lista `allow_origins`.

> **Por qué es necesario:** el navegador envía una petición `OPTIONS` (preflight) antes de cada llamada cross-origin. Sin el middleware, FastAPI respondía `405 Method Not Allowed` y bloqueaba todas las peticiones del frontend.

---

## Variables de entorno

Crea un fichero `.env` en la raíz del proyecto (o configura las variables en Docker Compose):

```env
# MongoDB
MONGO_URI=mongodb://admin:admin123@localhost:27017/ibermon_db?authSource=admin
MONGO_DB_NAME=ibermon_db

# JWT
SECRET_KEY=cambia_esto_en_produccion_por_algo_seguro
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# App
APP_NAME=ApiIbermon
DEBUG=False
```

---

## Puesta en marcha

### Local con uvicorn

**Requisitos:** Python 3.11+, MongoDB corriendo en `localhost:27017`.

```bash
# 1. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear .env con tus valores (ver sección anterior)

# 4. Poblar la BD (una de las dos opciones):
python -m app.utils.seed            # Datos de prueba del juego
python -m app.utils.seed_pokeapi    # 649 Pokémon de B&W (recomendado)

# 5. Arrancar el servidor
uvicorn app.main:app --reload
```

La API queda disponible en:
- **API:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

### Con Docker

El `docker-compose.yml` levanta tres servicios:

| Servicio | Puerto | Descripción |
|---|---|---|
| `ibermon_api` | 8000 | FastAPI + Uvicorn |
| `ibermon_mongodb` | 27017 | MongoDB 7.0 |
| `ibermon_seed` | — | Ejecuta seed.py una sola vez (perfil `seed`) |

```bash
# Construir y levantar API + MongoDB
docker-compose up -d

# Ejecutar seed de datos base (perfil seed)
docker-compose --profile seed up seed

# Ver logs
docker-compose logs -f api

# Parar todo
docker-compose down
```

> Para el seed de PokéAPI dentro de Docker, ejecutarlo desde el contenedor:
> ```bash
> docker-compose exec api python -m app.utils.seed_pokeapi
> ```

---

## Scripts de seed

### `seed.py` — Datos base del juego

Pobla la BD con datos de prueba creados manualmente para el juego Ibermon:

- **20 movimientos** propios del juego (Placaje, Ascuas, Hidrobomba…)
- **16 Ibermon** de prueba (incluyendo las líneas de Bulbasaur, Charmander, Squirtle y varios originales)
- **18 ítems** (pociones, balls, ítems de batalla, ítems clave)
- **14 logros**

```bash
python -m app.utils.seed
```

> Si ya hay datos en BD, el script los omite sin borrar nada.

---

### `seed_pokeapi.py` — Pokémon Black & White

Descarga automáticamente los **649 Pokémon de la era Black & White** (Gen 1–5) usando [PokéAPI](https://pokeapi.co) y los inserta en la BD como Ibermon.

**Datos obtenidos por cada Pokémon:**

| Dato | Fuente en PokéAPI | Notas |
|---|---|---|
| Nombre | `pokemon-species/{id}/names` | Prioriza español (`es`), fallback inglés |
| Tipos | `pokemon/{id}/types` | Traducidos al español |
| Estadísticas base | `pokemon/{id}/stats` | HP, ATK, DEF, SP.ATK, SP.DEF, VEL |
| Descripción | `pokemon-species/{id}/flavor_text_entries` | Texto del Pokédex en español |
| Movimientos nivel | `pokemon/{id}/moves` | Filtrados por Black/White version group |
| Cadena evolutiva | `evolution-chain/{id}` | `evoluciona_a` + `nivel_evolucion` |
| Sprite | `pokemon/{id}/sprites` | GIF animado Gen V BW → PNG BW → Official Art |
| Catch rate | `pokemon-species/{id}/capture_rate` | — |
| EXP yield | `pokemon/{id}/base_experience` | — |
| Curva de crecimiento | `pokemon-species/{id}/growth_rate` | Traducida al español |

**Movimientos insertados:** todos los movimientos únicos que aprende alguno de los 649 Pokémon por subida de nivel en Black/White (aproximadamente 400–500 movimientos).

**Uso:**

```bash
# Instalar httpx si no está
pip install httpx

# Seed completo (Gen 1–5, #1–649) — tarda ~5–8 minutos
python -m app.utils.seed_pokeapi

# Solo Gen 5 (Unova, #494–649)
python -m app.utils.seed_pokeapi --desde 494

# Solo un rango de prueba (rápido)
python -m app.utils.seed_pokeapi --desde 1 --hasta 9

# Borrar datos existentes y re-insertar todo
python -m app.utils.seed_pokeapi --force
```

**Parámetros:**

| Parámetro | Default | Descripción |
|---|---|---|
| `--desde N` | `1` | Número de Pokémon desde el que empezar |
| `--hasta N` | `649` | Número de Pokémon hasta el que llegar |
| `--force` | `False` | Vacía las colecciones antes de insertar |

**Salida esperada:**
```
════════════════════════════════════════════════════════
  Ibermon Seed — PokéAPI  Black & White  (#1–649)
════════════════════════════════════════════════════════

► Conectando a MongoDB...
  ✓ Conectado

► Fase 1/3 — Descargando 649 Pokémon + Especies...
  ✓ 649/649 Pokémon obtenidos

► Fase 2/3 — Cadenas evolutivas...
  ✓ 211 cadenas → 398 evoluciones mapeadas

► Fase 3/3 — Movimientos de nivel (Black & White)...
  Movimientos únicos encontrados: 468
  Descargando detalles...
  ✓ 468 movimientos insertados en BD

► Construyendo 649 Ibermon...
  [██████████████████████████████] 649/649  #649 Genesect
  Insertando en MongoDB...
  ✓ 649 Ibermon insertados en BD

════════════════════════════════════════════════════════
  ✓  Seed completado en 6m 32s
     Ibermon insertados  : 649
     Movimientos         : 468
     Evoluciones mapeadas: 398
════════════════════════════════════════════════════════
```

**Detalles técnicos:**
- Máximo 20 peticiones concurrentes a PokéAPI (`MAX_CONCURRENT = 20`)
- Reintentos exponenciales ante errores de red (hasta 4 intentos)
- Las cadenas evolutivas se cachean para no refetcharlas
- Los movimientos solo se insertan si son aprendidos por al menos un Pokémon
- Inserción en batches de 100 documentos

---

### `clean.py` — Borrar catálogos

Borra todas las colecciones de catálogo (ibermon, movimientos, ítems, logros) sin tocar usuarios ni partidas.

```bash
python -m app.utils.clean
```

> Útil para limpiar antes de un re-seed. También puedes usar `seed_pokeapi.py --force` que ya limpia e inserta en un solo paso.

---

## Documentación interactiva

Con la API corriendo, accede a la documentación generada automáticamente por FastAPI:

- **Swagger UI** → `http://localhost:8000/docs`
- **ReDoc** → `http://localhost:8000/redoc`

Ambas interfaces permiten probar todos los endpoints directamente desde el navegador, incluyendo autenticación JWT.
