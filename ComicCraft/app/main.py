from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.routes import router

settings = get_settings()

app = FastAPI(
    title="ComicCraft API",
    description="AI comic story creator using Gemini and diffusion image generation.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
