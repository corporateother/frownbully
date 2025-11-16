# this file will be used as our API app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

import image_processor as ip  # your logic

app = FastAPI()

# allow local access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# project root (where main.py lives)
BASE_DIR = Path(__file__).resolve().parent

# >>> IMPORTANT: use 'build' here, not 'dist'
FRONTEND_BUILD_DIR = BASE_DIR / "frontend" / "build"

# serve the built Vite app
if FRONTEND_BUILD_DIR.exists():
    # /assets/... -> frontend/build/assets/...
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_BUILD_DIR / "assets"),
        name="assets",
    )

    @app.get("/")
    async def serve_index():
        return FileResponse(FRONTEND_BUILD_DIR / "index.html")


# -------- API endpoints --------

@app.post("/api/start")
def api_start():
    ip.start_detection()
    return {"running": True}


@app.post("/api/stop")
def api_stop():
    ip.stop_detection()
    return {"running": False}


@app.get("/api/status")
def api_status():
    return {"running": ip.is_running()}


@app.get("/api/stats")
def api_stats():
    return ip.get_stats()
