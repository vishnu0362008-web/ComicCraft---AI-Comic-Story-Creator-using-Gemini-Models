# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI web application that turns a user's story idea into a 5-panel comic. It follows the project specification: collect prompt/character/setting/tone/art-style inputs, generate a structured outline, expand it into narration and dialogue, create panel artwork, build a layout, and export the result as PDF.

## Modernized implementation

The original documentation references the legacy `google-generativeai` package and Gemini 1.5 models. This implementation uses Google's current `google-genai` SDK and environment-configurable current model IDs. The image layer uses Hugging Face `InferenceClient` so Stable Diffusion runs remotely instead of requiring a large local model download. This is much easier to run on ordinary Windows laptops.

## Features

- FastAPI backend with HTML and JSON APIs
- Jinja2 frontend
- Structured Gemini JSON output validated with Pydantic
- Gemini outline + story generation
- Hugging Face Stable Diffusion image generation
- 5-panel comic layout
- Multi-page PDF export
- Download endpoint
- Developer image-test endpoint
- Demo mode for testing the application without AI credentials
- Automated unit tests for validation, parsing, layout and PDF generation

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_flash.py
│   │   ├── gemini_pro.py
│   │   ├── image_generator.py
│   │   ├── layout_builder.py
│   │   ├── exporters.py
│   │   └── demo_data.py
│   └── utils.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── css/style.css
│   ├── js/app.js
│   ├── panels/
│   └── exports/
├── tests/
│   └── test_core.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Quick start on Windows

1. Install Python 3.11 or 3.12.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. Create the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt and run:

```cmd
.venv\Scripts\activate.bat
```

5. Install packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Copy `.env.example` to `.env`.
7. Add your Gemini API key and Hugging Face token.
8. Start the server:

```powershell
uvicorn app.main:app --reload
```

9. Open:

- Web app: http://127.0.0.1:8000
- Swagger API: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Demo mode

To test the full browser/PDF flow before configuring AI providers, set:

```env
DEMO_MODE=true
```

Then run the server. The app uses deterministic sample comic data and generated placeholder artwork. Switch it back to `false` for real Gemini + Stable Diffusion generation.

## API

### POST `/generate-comic/json`

Example:

```json
{
  "story_prompt": "A brave fox explores an enchanted forest and discovers a hidden library.",
  "character_name": "Kavi",
  "setting": "Enchanted forest",
  "tone": "dramatic",
  "art_style": "comic book"
}
```

### POST `/test-image`

```json
{"prompt":"A brave fox in an enchanted forest, comic book illustration"}
```

## Testing

Run:

```powershell
pytest -q
```

The tests intentionally do not call paid AI services.

## Production notes

- Keep `.env` out of Git.
- Use a persistent object store for images in production.
- Add authentication/rate limiting before exposing generation publicly.
- Move long-running generation into a job queue for multi-user deployments.
- Pin tested dependency versions before production deployment.
