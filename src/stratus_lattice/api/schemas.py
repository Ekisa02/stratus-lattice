from typing import List, Optional
from pydantic import BaseModel


class LoadModelRequest(BaseModel):
    name: str
    input_dim: int


class InferRequest(BaseModel):
    model: str
    data: List[float]
    distribute: Optional[bool] = False


class InferResponse(BaseModel):
    model: str
    output: List[float]
    node: str


class PeersResponse(BaseModel):
    peers: List[str]
