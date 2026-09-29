from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image
from app.config import get_settings
from app.models import LayoutPanel

def _resolve_image(image_path: str, static_dir: Path) -> Path:
    relative = urlparse(image_path).path.removeprefix("/static/")
    path = (static_dir / relative).resolve()
    if static_dir.resolve() not in path.parents:
        raise ValueError("Invalid image path")
    if not path.exists():
        raise FileNotFoundError(path)
    return path

def _pdf_text(value: str) -> str:
    """FPDF core Helvetica fonts are limited to Latin-1; replace unsupported Unicode safely."""
    return str(value).encode("latin-1", "replace").decode("latin-1")

def save_pdf(layout: list[LayoutPanel]) -> str:
    from fpdf import FPDF
    settings = get_settings()
    export_dir = settings.static_dir / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    filename = f"comiccraft-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.pdf"
    output = export_dir / filename
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "ComicCraft", align="C")
        pdf.ln(10)
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 14)
        pdf.multi_cell(0, 8, _pdf_text(f"Panel {panel.panel_number}: {panel.title}"))
        pdf.ln(3)
        image_file = _resolve_image(panel.image_path, settings.static_dir)
        with Image.open(image_file) as img:
            width, height = img.size
        max_w, max_h = 180, 105
        scale = min(max_w / width, max_h / height)
        pdf.image(str(image_file), x=(210 - width * scale) / 2, w=width * scale)
        pdf.ln(6)
        pdf.set_x(15)
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 6, _pdf_text(panel.scene_description))
        pdf.ln(2)
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 6, _pdf_text(f"Caption: {panel.caption}"))
        pdf.set_x(15)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, _pdf_text(f"Narration: {panel.narration}"))
        if panel.dialogue:
            pdf.ln(2)
            pdf.set_x(15)
            pdf.set_font("Helvetica", "I", 11)
            pdf.multi_cell(0, 7, _pdf_text(f"Dialogue: {panel.dialogue}"))
    pdf.output(str(output))
    return "/static/exports/" + filename
