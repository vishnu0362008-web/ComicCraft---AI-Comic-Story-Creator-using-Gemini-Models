from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from app.config import get_settings
from app.utils import safe_filename, public_static_path

def _placeholder(prompt: str, output_path: Path) -> None:
    image = Image.new("RGB", (768,512), "#f3efe4"); draw=ImageDraw.Draw(image)
    draw.rectangle((18,18,750,494), outline="#191919", width=8)
    try: font=ImageFont.truetype("arial.ttf",32)
    except OSError: font=ImageFont.load_default()
    draw.text((45,45),"COMICCRAFT DEMO PANEL",fill="#191919",font=font)
    draw.text((45,115),prompt[:220],fill="#333333",font=font)
    draw.ellipse((520,235,690,405),outline="#191919",width=7); draw.arc((555,275,655,355),0,180,fill="#191919",width=5)
    image.save(output_path,"PNG")

def generate_image(prompt: str) -> str:
    s=get_settings(); out=s.static_dir/"panels"; out.mkdir(parents=True,exist_ok=True); path=out/safe_filename(prompt)
    if s.demo_mode:
        _placeholder(prompt,path); return public_static_path(path,s.static_dir)
    if not s.hf_token: raise RuntimeError("HF_TOKEN is not configured. Add it to .env or enable DEMO_MODE.")
    from huggingface_hub import InferenceClient
    client=InferenceClient(api_key=s.hf_token,provider="auto")
    image=client.text_to_image(prompt=prompt,model=s.hf_image_model,width=s.image_width,height=s.image_height,num_inference_steps=s.image_steps,negative_prompt="blurry, low quality, distorted anatomy, extra fingers, unreadable text, watermark, logo")
    if not isinstance(image,Image.Image): raise RuntimeError("Hugging Face did not return a PIL image")
    image.save(path,"PNG"); return public_static_path(path,s.static_dir)
