import re
from pathlib import Path
from uuid import uuid4


def safe_filename(value: str, suffix: str = ".png") -> str:
    stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.lower()).strip("-")[:60] or "panel"
    return f"{stem}-{uuid4().hex[:10]}{suffix}"


def public_static_path(path: Path, static_dir: Path) -> str:
    return "/static/" + path.relative_to(static_dir).as_posix()
