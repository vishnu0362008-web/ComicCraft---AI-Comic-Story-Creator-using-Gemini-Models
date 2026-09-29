from app.config import get_settings
from app.models import ComicOutline, ComicStory, PromptRequest

def _client():
    key = get_settings().gemini_api_key
    if not key: raise RuntimeError("GEMINI_API_KEY is not configured")
    from google import genai
    return genai.Client(api_key=key)

def generate_story(request: PromptRequest, outline: ComicOutline) -> ComicStory:
    s = get_settings()
    prompt = f'''Expand this five-panel comic outline into a polished comic story.\nOriginal story prompt: {request.story_prompt}\nCharacter: {request.character_name}\nSetting: {request.setting}\nTone: {request.tone}\nArt style: {request.art_style}\nOutline JSON:\n{outline.model_dump_json()}\nRules: Preserve exactly five panels and their order. Each panel needs concise scene description, caption, narration, and natural dialogue. Keep character names and continuity consistent. Keep dialogue short enough to fit a comic panel. Return valid structured data only.'''
    response = _client().models.generate_content(model=s.gemini_story_model, contents=prompt, config={"response_mime_type":"application/json","response_schema":ComicStory,"temperature":0.85})
    return response.parsed if isinstance(getattr(response,"parsed",None), ComicStory) else ComicStory.model_validate_json(response.text)
