import pytest
import torch
from src.stratus_lattice.models.model_zoo import TinyModel, register_model, get_model, infer


def test_tiny_model_forward():
    m = TinyModel(input_dim=4, hidden=8, out_dim=2)
    register_model("t1", m)
    model = get_model("t1")
    assert model is not None
    out = infer(model, [0.1, 0.2, 0.3, 0.4])
    assert isinstance(out, list)
    assert len(out) == 2
