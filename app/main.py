from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.analyze import router as analyze_router

load_dotenv()

app = FastAPI(title="GainesAI Thin Slice")

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(analyze_router)


@app.get("/")
async def read_index() -> FileResponse:
    return FileResponse(static_dir / "index.html")
