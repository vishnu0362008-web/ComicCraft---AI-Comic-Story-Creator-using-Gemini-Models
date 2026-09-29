from app.config import get_settings
from app.models import ComicOutline, PromptRequest

def _client():
    key = get_settings().gemini_api_key
    if not key: raise RuntimeError("GEMINI_API_KEY is not configured")
    from google import genai
    return genai.Client(api_key=key)

def generate_outline(request: PromptRequest) -> ComicOutline:
    s = get_settings()
    prompt = f'''Create exactly five sequential comic panels for this idea.\nStory prompt: {request.story_prompt}\nMain character: {request.character_name}\nSetting: {request.setting}\nTone: {request.tone}\nArt style: {request.art_style}\nReturn a coherent beginning, escalation, turning point and ending. Keep the same main character and visual identity across panels. Image prompts must describe only what should appear visually and must be suitable for a text-to-image diffusion model. Do not include readable speech bubbles in the image prompt.'''
    response = _client().models.generate_content(model=s.gemini_outline_model, contents=prompt, config={"response_mime_type":"application/json","response_schema":ComicOutline,"temperature":0.9})
    return response.parsed if isinstance(getattr(response,"parsed",None), ComicOutline) else ComicOutline.model_validate_json(response.text)
