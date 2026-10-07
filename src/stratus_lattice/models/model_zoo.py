from typing import Dict, List
import torch
import torch.nn as nn
import torch.nn.functional as F


class TinyModel(nn.Module):
    def __init__(self, input_dim: int = 8, hidden: int = 16, out_dim: int = 4):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden)
        self.fc2 = nn.Linear(hidden, out_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


_REGISTRY: Dict[str, nn.Module] = {}


def register_model(name: str, model: nn.Module):
    _REGISTRY[name] = model.eval()


def get_model(name: str):
    return _REGISTRY.get(name)


def infer(model: nn.Module, data: List[float]) -> List[float]:
    # Simple conversion: list[float] to tensor
    import torch
    t = torch.tensor(data, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        out = model(t)
    return out.squeeze(0).tolist()


def save_model(name: str, path: str):
    model = get_model(name)
    if model is None:
        raise ValueError("model not found")
    torch.save(model.state_dict(), path)


def load_model(name: str, cls, path: str):
    model = cls()
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    register_model(name, model)
