import os
os.environ["DEMO_MODE"] = "true"

from fastapi.testclient import TestClient
from app.main import app
from app.models import PromptRequest
from app.services.demo_data import demo_outline, demo_story
from app.services.layout_builder import build_comic_layout


def sample_request():
    return PromptRequest(
        story_prompt="A brave fox explores an enchanted forest and discovers a hidden library.",
        character_name="Kavi",
        setting="Enchanted forest",
        tone="dramatic",
        art_style="comic book",
    )


def test_home():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "ComicCraft" in response.text


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_demo_outline_and_story_have_five_panels():
    request = sample_request()
    outline = demo_outline(request)
    story = demo_story(request, outline)
    assert len(outline.panels) == 5
    assert len(story.panels) == 5
    assert [p.panel_number for p in story.panels] == [1,2,3,4,5]


def test_layout_pairs_images_and_story():
    request = sample_request()
    story = demo_story(request, demo_outline(request))
    paths = [f"/static/panels/panel-{i}.png" for i in range(1, 6)]
    layout = build_comic_layout(story, paths)
    assert len(layout) == 5
    assert layout[2].image_path.endswith("panel-3.png")


def test_json_generation_demo(tmp_path, monkeypatch):
    # Replace generated image/PDF functions with local test-safe implementations.
    import app.routes as routes
    monkeypatch.setattr(routes, "generate_image", lambda prompt: "/static/panels/test.png")
    monkeypatch.setattr(routes, "save_pdf", lambda layout: "/static/exports/test.pdf")
    client = TestClient(app)
    response = client.post("/generate-comic/json", json=sample_request().model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["layout"]) == 5
