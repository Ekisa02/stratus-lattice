import pytest
from fastapi.testclient import TestClient
from src.stratus_lattice.app import create_app
from src.stratus_lattice.models.model_zoo import TinyModel, register_model


client = TestClient(create_app())


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_load_and_infer_local():
    # register a model directly and call /infer
    register_model("tiny_test", TinyModel(input_dim=3, hidden=4, out_dim=1))
    payload = {"model": "tiny_test", "data": [0.1, 0.2, 0.3], "distribute": False}
    r = client.post("/infer", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["model"] == "tiny_test"
    assert isinstance(data["output"], list)
    assert data["node"].startswith("node-") or isinstance(data["node"], str)
