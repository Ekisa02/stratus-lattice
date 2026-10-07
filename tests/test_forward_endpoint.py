import pytest
from fastapi.testclient import TestClient
from src.stratus_lattice.app import create_app
from src.stratus_lattice.models.model_zoo import TinyModel, register_model

client = TestClient(create_app())


def test_forward_endpoint_local():
    register_model("fwd_test", TinyModel(input_dim=2, hidden=4, out_dim=2))
    payload = {"model": "fwd_test", "data": [0.5, 0.6]}
    r = client.post("/forward", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert j["model"] == "fwd_test"
    assert "node" in j
    assert isinstance(j["output"], list)
