from typing import List
from pydantic import BaseModel, Field, field_validator

class PromptRequest(BaseModel):
    story_prompt: str = Field(..., min_length=5, max_length=2000)
    character_name: str = Field(..., min_length=1, max_length=80)
    setting: str = Field(..., min_length=1, max_length=120)
    tone: str = Field(..., min_length=1, max_length=50)
    art_style: str = Field(..., min_length=1, max_length=80)

    @field_validator("story_prompt", "character_name", "setting", "tone", "art_style")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty")
        return value

class PanelOutline(BaseModel):
    panel_number: int = Field(..., ge=1, le=5)
    title: str = Field(..., min_length=1, max_length=120)
    scene_description: str = Field(..., min_length=1, max_length=1000)
    image_prompt: str = Field(..., min_length=1, max_length=1500)

class ComicOutline(BaseModel):
    panels: List[PanelOutline] = Field(..., min_length=5, max_length=5)

class StoryPanel(BaseModel):
    panel_number: int = Field(..., ge=1, le=5)
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str = ""
    image_prompt: str

class ComicStory(BaseModel):
    panels: List[StoryPanel] = Field(..., min_length=5, max_length=5)

class LayoutPanel(BaseModel):
    panel_number: int
    title: str
    image_path: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str
    image_prompt: str

class ImageTestRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=1500)
