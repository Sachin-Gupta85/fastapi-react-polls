"""API tests for the Polls service (in-memory mongomock)."""
import mongomock
import pytest
from fastapi.testclient import TestClient

from app.db import get_db
from app.main import app


@pytest.fixture
def client():
    db = mongomock.MongoClient()["testdb"]
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _make(client, q="Best?", opts=("A", "B", "C")):
    return client.post("/api/polls", json={"question": q, "options": list(opts)}).json()


def test_create_initializes_zero_votes(client):
    p = _make(client)
    assert p["total_votes"] == 0
    assert [o["votes"] for o in p["options"]] == [0, 0, 0]


def test_create_requires_two_options(client):
    assert client.post("/api/polls", json={"question": "x", "options": ["only"]}).status_code == 422
    assert client.post("/api/polls", json={"question": "x", "options": ["a", "  "]}).status_code == 422


def test_voting_increments_and_totals(client):
    pid = _make(client)["id"]
    client.post(f"/api/polls/{pid}/vote", json={"option": 0})
    client.post(f"/api/polls/{pid}/vote", json={"option": 0})
    out = client.post(f"/api/polls/{pid}/vote", json={"option": 2}).json()
    assert [o["votes"] for o in out["options"]] == [2, 0, 1]
    assert out["total_votes"] == 3


def test_vote_out_of_range_is_400(client):
    pid = _make(client)["id"]
    assert client.post(f"/api/polls/{pid}/vote", json={"option": 9}).status_code == 400
    assert client.post(f"/api/polls/{pid}/vote", json={"option": -1}).status_code == 422


def test_list_delete_and_404(client):
    pid = _make(client)["id"]
    assert len(client.get("/api/polls").json()) == 1
    assert client.delete(f"/api/polls/{pid}").status_code == 204
    assert client.get(f"/api/polls/{pid}").status_code == 404
    assert client.post("/api/polls/nope/vote", json={"option": 0}).status_code == 404
