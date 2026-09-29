from app.models import ComicStory, LayoutPanel

def build_comic_layout(story: ComicStory, image_paths: list[str]) -> list[LayoutPanel]:
    if len(story.panels)!=len(image_paths): raise ValueError("Every story panel must have exactly one generated image")
    return [LayoutPanel(panel_number=p.panel_number,title=p.title,image_path=image_paths[i],scene_description=p.scene_description,caption=p.caption,narration=p.narration,dialogue=p.dialogue,image_prompt=p.image_prompt) for i,p in enumerate(story.panels)]
