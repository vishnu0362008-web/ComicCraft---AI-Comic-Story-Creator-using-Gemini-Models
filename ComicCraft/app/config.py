from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    host: str = "127.0.0.1"
    port: int = 8000
    gemini_api_key: str = ""
    hf_token: str = ""
    gemini_outline_model: str = "gemini-3.8-flash"
    gemini_story_model: str = "gemini-3.1-pro-preview"
    hf_image_model: str = "stabilityai/stable-diffusion-3-medium-diffusers"
    demo_mode: bool = False
    image_width: int = 768
    image_height: int = 512
    image_steps: int = 28
    max_prompt_length: int = 2000
    base_dir: Path = BASE_DIR
    static_dir: Path = BASE_DIR / "static"
    template_dir: Path = BASE_DIR / "templates"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
