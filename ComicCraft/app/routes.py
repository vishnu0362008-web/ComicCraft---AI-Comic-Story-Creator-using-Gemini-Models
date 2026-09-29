from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.models import ImageTestRequest, PromptRequest
from app.services.demo_data import demo_outline, demo_story
from app.services.exporters import save_pdf
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.utils import public_static_path

router = APIRouter()
settings = get_settings()
templates = Jinja2Templates(directory=str(settings.template_dir))


def _generate(request_data: PromptRequest):
    if settings.demo_mode:
        outline = demo_outline(request_data)
        story = demo_story(request_data, outline)
    else:
        outline = generate_outline(request_data)
        story = generate_story(request_data, outline)
    image_paths = [generate_image(panel.image_prompt) for panel in story.panels]
    layout = build_comic_layout(story, image_paths)
    pdf_path = save_pdf(layout)
    return outline, story, layout, pdf_path


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"demo_mode": settings.demo_mode})


@router.get("/health")
async def health():
    return {"status": "ok", "demo_mode": settings.demo_mode, "app": settings.app_name}


@router.post("/generate")
async def generate_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        data = PromptRequest(story_prompt=story_prompt, character_name=character_name, setting=setting, tone=tone, art_style=art_style)
        outline, story, layout, pdf_path = _generate(data)
        return templates.TemplateResponse(request=request, name="comic_preview.html", context={
            "layout": layout, "pdf_path": pdf_path, "request_data": data, "demo_mode": settings.demo_mode,
        })
    except Exception as exc:
        return templates.TemplateResponse(request=request, name="index.html", context={
            "demo_mode": settings.demo_mode, "error": str(exc),
            "form_data": {"story_prompt": story_prompt, "character_name": character_name, "setting": setting, "tone": tone, "art_style": art_style},
        }, status_code=500)


@router.post("/generate-comic/json")
async def generate_json(data: PromptRequest):
    try:
        outline, story, layout, pdf_path = _generate(data)
        return {"success": True, "outline": outline.model_dump(), "story": story.model_dump(), "layout": [p.model_dump() for p in layout], "pdf_path": pdf_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/test-image")
async def test_image(data: ImageTestRequest):
    try:
        path = generate_image(data.prompt)
        return {"success": True, "image_path": path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/export-success")
async def export_success(request: Request, pdf_path: str = ""):
    return templates.TemplateResponse(request=request, name="export_success.html", context={"pdf_path": pdf_path})


@router.get("/download")
async def download(pdf_path: str):
    if not pdf_path.startswith("/static/exports/"):
        raise HTTPException(status_code=400, detail="Invalid export path")
    file_path = settings.static_dir / pdf_path.removeprefix("/static/")
    if not file_path.exists() or file_path.suffix.lower() != ".pdf":
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(file_path, media_type="application/pdf", filename=file_path.name)
