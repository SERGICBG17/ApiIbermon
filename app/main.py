from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.responses import HTMLResponse

from app.core.config import settings
from app.db.session import connect_db
from app.routers import auth_router, partida_router, ibermon_jugador_router, catalogo_router, item_jugador_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="API REST del videojuego Ibermon 2D",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router.router)
app.include_router(partida_router.router)
app.include_router(ibermon_jugador_router.router)
app.include_router(item_jugador_router.router)
app.include_router(catalogo_router.router)


@app.get("/", response_class=HTMLResponse)
def html():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Ibermon API</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;600;700&display=swap');

            .font-pixel { font-family: 'Press Start 2P', monospace; }

            /* Pokeball spinner */
            @keyframes spin-ball { to { transform: rotate(360deg); } }
            .pokeball { animation: spin-ball 3s linear infinite; }

            /* Pixel border */
            .pixel-border {
                box-shadow:
                    0 -4px 0 0 #1e293b,
                    0  4px 0 0 #1e293b,
                    -4px 0 0 0 #1e293b,
                     4px 0 0 0 #1e293b;
            }

            /* Scanlines overlay */
            .scanlines::after {
                content: '';
                position: absolute;
                inset: 0;
                background: repeating-linear-gradient(
                    to bottom,
                    transparent 0px,
                    transparent 3px,
                    rgba(0,0,0,0.08) 3px,
                    rgba(0,0,0,0.08) 4px
                );
                pointer-events: none;
                border-radius: inherit;
            }

            /* HP bar fill animation */
            @keyframes hp-fill { from { width: 0%; } to { width: 73%; } }
            .hp-fill { animation: hp-fill 1.4s ease-out 0.5s both; }

            /* Floating animation for cards */
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50%       { transform: translateY(-4px); }
            }
            .float-1 { animation: float 3.2s ease-in-out infinite; }
            .float-2 { animation: float 3.8s ease-in-out 0.6s infinite; }
            .float-3 { animation: float 3.5s ease-in-out 1.2s infinite; }

            /* Cursor blink */
            @keyframes blink { 50% { opacity: 0; } }
            .blink { animation: blink 1s step-end infinite; }

            /* Stardust particles */
            @keyframes rise {
                0%   { transform: translateY(0) scale(1);   opacity: 1; }
                100% { transform: translateY(-60px) scale(0); opacity: 0; }
            }
            .particle { animation: rise linear infinite; }
        </style>
    </head>
    <body class="min-h-screen font-sans text-slate-800 overflow-x-hidden"
          style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);">

        <!-- Stars background -->
        <div class="fixed inset-0 overflow-hidden pointer-events-none" id="stars"></div>

        <!-- Main container -->
        <div class="relative z-10 flex flex-col items-center justify-center min-h-screen px-4 py-16">

            <!-- Header badge -->
            <div class="font-pixel text-yellow-400 text-xs mb-6 tracking-widest opacity-80">
                ★ &nbsp;IBERMON WORLD&nbsp; ★
            </div>

            <!-- Main card -->
            <div class="relative bg-slate-900 rounded-2xl pixel-border w-full max-w-lg overflow-hidden scanlines">

                <!-- Top red stripe with Pokeball -->
                <div class="relative bg-red-600 px-6 pt-6 pb-10">
                    <!-- White divider line -->
                    <div class="absolute bottom-0 left-0 right-0 h-3 bg-white"></div>
                    <div class="absolute bottom-0 left-0 right-0 h-1 bg-slate-900 translate-y-full"></div>

                    <!-- Pokeball center button -->
                    <div class="absolute -bottom-5 left-1/2 -translate-x-1/2 z-10
                                w-10 h-10 rounded-full bg-white border-4 border-slate-900
                                flex items-center justify-center">
                        <div class="w-4 h-4 rounded-full bg-white border-2 border-slate-700"></div>
                    </div>

                    <div class="flex items-start justify-between">
                        <div>
                            <p class="font-pixel text-white text-xs opacity-70 mb-1">v1.0.0</p>
                            <h1 class="font-pixel text-white text-lg leading-relaxed">
                                Ibermon<br>
                                <span class="text-yellow-300">API</span>
                            </h1>
                        </div>
                        <!-- Spinning pokeball SVG -->
                        <svg class="pokeball w-16 h-16 opacity-30" viewBox="0 0 100 100" fill="none">
                            <circle cx="50" cy="50" r="48" stroke="white" stroke-width="4"/>
                            <path d="M2 50 h96" stroke="white" stroke-width="4"/>
                            <path d="M2 50 Q2 2 50 2 Q98 2 98 50" fill="rgba(255,255,255,0.15)"/>
                            <circle cx="50" cy="50" r="14" fill="none" stroke="white" stroke-width="4"/>
                            <circle cx="50" cy="50" r="7" fill="white"/>
                        </svg>
                    </div>
                </div>

                <!-- Body -->
                <div class="px-6 pt-10 pb-6 bg-slate-900">

                    <!-- Status row -->
                    <div class="flex items-center gap-3 mb-6">
                        <span class="w-2 h-2 rounded-full bg-green-400 shadow-[0_0_6px_#4ade80]"></span>
                        <span class="text-green-400 text-sm font-semibold tracking-wide">Servidor operativo</span>
                        <span class="ml-auto font-pixel text-slate-500 text-xs">FastAPI · MongoDB</span>
                    </div>

                    <!-- HP bar (decorative) -->
                    <div class="mb-6 bg-slate-800 rounded-lg p-3">
                        <div class="flex justify-between text-xs text-slate-400 mb-1">
                            <span class="font-pixel" style="font-size:9px">SERVER HP</span>
                            <span class="font-pixel text-green-400" style="font-size:9px">73 / 100</span>
                        </div>
                        <div class="h-3 bg-slate-700 rounded-full overflow-hidden">
                            <div class="hp-fill h-full rounded-full"
                                 style="background: linear-gradient(90deg, #4ade80, #22c55e);"></div>
                        </div>
                    </div>

                    <!-- Stat cards -->
                    <div class="grid grid-cols-3 gap-3 mb-6">
                        <div class="float-1 bg-slate-800 rounded-xl p-3 text-center border border-slate-700">
                            <div class="text-2xl mb-1">⚔️</div>
                            <div class="font-pixel text-yellow-400" style="font-size:9px">Rutas</div>
                            <div class="text-white font-bold text-lg mt-1">5</div>
                        </div>
                        <div class="float-2 bg-slate-800 rounded-xl p-3 text-center border border-slate-700">
                            <div class="text-2xl mb-1">🛡️</div>
                            <div class="font-pixel text-yellow-400" style="font-size:9px">Auth JWT</div>
                            <div class="text-green-400 font-bold text-lg mt-1">ON</div>
                        </div>
                        <div class="float-3 bg-slate-800 rounded-xl p-3 text-center border border-slate-700">
                            <div class="text-2xl mb-1">🎮</div>
                            <div class="font-pixel text-yellow-400" style="font-size:9px">Versión</div>
                            <div class="text-white font-bold text-lg mt-1">1.0</div>
                        </div>
                    </div>

                    <!-- Dialogue box style description -->
                    <div class="relative bg-slate-800 border-2 border-slate-600 rounded-lg p-4 mb-6">
                        <div class="absolute -top-3 left-4 bg-slate-900 px-2">
                            <span class="font-pixel text-yellow-400" style="font-size:9px">PROFESOR IB</span>
                        </div>
                        <p class="text-slate-300 text-sm leading-relaxed">
                            ¡Bienvenido al mundo de <span class="text-yellow-400 font-semibold">Ibermon</span>!
                            Esta API REST gestiona partidas, equipos, catálogos y combates.
                        </p>
                        <span class="blink text-slate-400 text-lg absolute bottom-3 right-4">▼</span>
                    </div>

                    <!-- Action buttons -->
                    <div class="grid grid-cols-2 gap-3">
                        <a href="/docs"
                           class="group relative overflow-hidden flex items-center justify-center gap-2
                                  bg-red-600 hover:bg-red-500 text-white font-bold py-3 px-4
                                  rounded-xl transition-all duration-200 pixel-border text-sm">
                            <span class="text-lg">📖</span>
                            <span class="font-pixel" style="font-size:9px">Swagger</span>
                        </a>
                        <a href="/redoc"
                           class="group relative overflow-hidden flex items-center justify-center gap-2
                                  bg-slate-700 hover:bg-slate-600 text-white font-bold py-3 px-4
                                  rounded-xl transition-all duration-200 pixel-border text-sm">
                            <span class="text-lg">📋</span>
                            <span class="font-pixel" style="font-size:9px">ReDoc</span>
                        </a>
                    </div>
                </div>

                <!-- Footer -->
                <div class="bg-slate-950 px-6 py-3 flex justify-between items-center">
                    <span class="font-pixel text-slate-600" style="font-size:8px">IBERMON © 2026</span>
                    <div class="flex gap-1">
                        <span class="w-2 h-2 rounded-full bg-red-500"></span>
                        <span class="w-2 h-2 rounded-full bg-yellow-500"></span>
                        <span class="w-2 h-2 rounded-full bg-green-500"></span>
                    </div>
                </div>
            </div>

            <!-- Bottom hint -->
            <p class="font-pixel text-slate-600 text-center mt-8" style="font-size:8px">
                PRESS START TO PLAY
                <span class="blink">_</span>
            </p>
        </div>

        <script>
            // Generate random stars
            const starsEl = document.getElementById('stars');
            for (let i = 0; i < 120; i++) {
                const s = document.createElement('div');
                const size = Math.random() < 0.8 ? 1 : 2;
                s.style.cssText = `
                    position:absolute;
                    width:${size}px; height:${size}px;
                    border-radius:50%;
                    background:white;
                    opacity:${(Math.random() * 0.5 + 0.2).toFixed(2)};
                    top:${(Math.random()*100).toFixed(2)}%;
                    left:${(Math.random()*100).toFixed(2)}%;
                    animation: blink ${(Math.random()*3+2).toFixed(1)}s ${(Math.random()*3).toFixed(1)}s ease-in-out infinite alternate;
                `;
                starsEl.appendChild(s);
            }
        </script>
    </body>
    </html>
    """
