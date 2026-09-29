from app.models import ComicOutline, ComicStory, PromptRequest

def demo_outline(request: PromptRequest) -> ComicOutline:
    p, s = request.character_name, request.setting
    return ComicOutline(panels=[
        {"panel_number":1,"title":"The Beginning","scene_description":f"{p} arrives at the {s}, sensing that something unusual is nearby.","image_prompt":f"{p} entering a mysterious {s}, cinematic comic book illustration, {request.art_style}, expressive character, detailed environment"},
        {"panel_number":2,"title":"The Discovery","scene_description":f"A strange clue appears and pulls {p} deeper into the {s}.","image_prompt":f"{p} discovering a mysterious clue in the {s}, {request.art_style} comic panel, dramatic lighting, dynamic composition"},
        {"panel_number":3,"title":"The Challenge","scene_description":f"{p} faces the central obstacle and must decide whether to continue.","image_prompt":f"{p} facing a dramatic obstacle in the {s}, {request.art_style}, comic book action panel, strong perspective"},
        {"panel_number":4,"title":"The Turning Point","scene_description":f"{p} finds a clever way forward and changes the course of the adventure.","image_prompt":f"{p} making a brave breakthrough in the {s}, heroic {request.art_style} comic illustration, dramatic atmosphere"},
        {"panel_number":5,"title":"A New Dawn","scene_description":f"The adventure ends with {p} changed by what happened in the {s}.","image_prompt":f"{p} standing triumphantly in the {s} at dawn, hopeful ending, {request.art_style} comic book illustration, beautiful lighting"},
    ])

def demo_story(request: PromptRequest, outline: ComicOutline) -> ComicStory:
    return ComicStory(panels=[{**p.model_dump(),"caption":f"{request.setting} — {p.title}.","narration":f"{request.character_name} took a breath and stepped forward. The {request.tone} journey was only beginning.","dialogue":f'"I have to see this through," said {request.character_name}.'} for p in outline.panels])
