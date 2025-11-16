import webview
import uvicorn
import threading
import time
import logging  # Added for better practice
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

# Assuming image_processor.py exists and handles the logic
import image_processor as ip

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION ---
HOST = "127.0.0.1"
PORT = 5000

app = FastAPI()

# Allow local access (CORS settings)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project root (where main.py lives, which appears to be 'root/backend')
BASE_DIR = Path(__file__).resolve().parent

# Correct path for the built frontend: 'root/frontend/build'
FRONTEND_BUILD_DIR = BASE_DIR.parent / "frontend" / "build"

# --- Frontend Serving Logic ---

if FRONTEND_BUILD_DIR.is_dir() and (FRONTEND_BUILD_DIR / "index.html").is_file():
    logging.info(f"Serving frontend from: {FRONTEND_BUILD_DIR}")

    # Mount static assets (like JS, CSS, images) from the /assets folder
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_BUILD_DIR / "assets"),
        name="assets",
    )


    # Main route: serve the index.html file
    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(FRONTEND_BUILD_DIR / "index.html")

else:
    logging.error(f"Frontend build directory not found or index.html missing: {FRONTEND_BUILD_DIR}")


    # Fallback route: show a Not Found JSON if the build doesn't exist
    @app.get("/", include_in_schema=False)
    async def serve_error():
        return JSONResponse(
            status_code=404,
            content={"detail": "Frontend build not found. Please run your build process first."}
        )


# -------- API endpoints --------

@app.post("/api/start")
def api_start():
    # Note: Ensure ip.start_detection() is thread-safe or non-blocking
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


# -------- Desktop Window Integration --------

def start_api_server():
    """Starts Uvicorn in the current thread."""
    # Use reload=False in production for stability
    uvicorn.run(app, host=HOST, port=PORT, log_level='warning')


if __name__ == "__main__":
    # 1. Start Uvicorn in a separate thread
    api_thread = threading.Thread(target=start_api_server, daemon=True)
    api_thread.start()

    # Give the server a moment to start up before launching the window
    # Without this, pywebview might launch before the socket is ready
    time.sleep(1)

    # 2. Create the native window, pointing it to the local Uvicorn address
    webview.create_window(
        "Frown Bully",
        url=f"http://{HOST}:{PORT}/",  # Use the explicit URL
        width=600,
        height=800,
        min_size=(400, 400),
        resizable=False
    )

    # 3. Start the PyWebView GUI loop. This is a blocking call.
    webview.start()

    # Optional: Clean up after the window is closed
    logging.info("Application closed. Stopping detection logic.")
    ip.stop_detection()