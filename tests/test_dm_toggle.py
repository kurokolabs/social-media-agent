"""Tests for Instagram DM automation toggle and webhook guard."""
import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("USE_MOCK_APIS", "true")
os.environ["IG_DM_AUTOMATION_ENABLED"] = "false"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("IG_DM_AUTOMATION_ENABLED", "false")

    from storage.database import initialize, initialize_social
    initialize()
    initialize_social()

    from api.app import app
    return TestClient(app)


def test_webhook_returns_disabled_when_off(client):
    resp = client.post("/webhooks/instagram", json={"entry": []})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "dm_automation_disabled"


def test_webhook_verify_returns_disabled_when_off(client):
    resp = client.get(
        "/webhooks/instagram",
        params={"hub.mode": "subscribe", "hub.verify_token": "x", "hub.challenge": "abc"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "dm_automation_disabled"


def test_settings_page_loads(client):
    resp = client.get("/settings")
    assert resp.status_code == 200
    assert "DM-Automation" in resp.text


def test_dm_toggle_off_returns_not_configured(client):
    resp = client.post("/settings/dm-toggle", data={})
    assert resp.status_code == 200
    # enabled checkbox not submitted → treated as off
    assert "Nicht konfiguriert" in resp.text or "aktivierbar" in resp.text or "Aktiv" in resp.text
