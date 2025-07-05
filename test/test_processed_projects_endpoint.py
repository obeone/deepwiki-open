from fastapi.testclient import TestClient

import api.api as api_app


def test_create_and_list_projects(tmp_path, monkeypatch):
    """Verify processed project creation and listing endpoints."""
    # Redirect cache directory to temporary path
    monkeypatch.setattr(api_app, 'WIKI_CACHE_DIR', tmp_path)

    client = TestClient(api_app.app)
    payload = {"repo_url": "https://github.com/example/repo", "repo_type": "github"}

    response = client.post("/api/processed_projects", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "Project registered"}

    created_files = list(tmp_path.iterdir())
    assert len(created_files) == 1

    list_resp = client.get("/api/processed_projects")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert data
    assert data[0]["owner"] == "example"
    assert data[0]["repo"] == "repo"
