from fastapi.testclient import TestClient

from fantasy.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_schema_is_generated() -> None:
    """The frontend's TypeScript client is generated from this schema, so if it
    stops building, the contract check in CI has nothing to compare against."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/health" in response.json()["paths"]
