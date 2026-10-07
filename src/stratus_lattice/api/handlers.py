from fastapi import APIRouter, HTTPException, Request
from typing import List
from ..api.schemas import LoadModelRequest, InferRequest, InferResponse, PeersResponse
from ..models import model_zoo
from ..discovery import discovery
from ..serving import serving
from ..config import get_node_name, get_peers

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/peers", response_model=PeersResponse)
async def peers():
    return PeersResponse(peers=get_peers())


@router.post("/load_model")
async def load_model(req: LoadModelRequest):
    # Create and register a tiny model
    model = model_zoo.TinyModel(req.input_dim)
    model_zoo.register_model(req.name, model)
    return {"status": "loaded", "model": req.name}


@router.post("/infer", response_model=InferResponse)
async def infer(req: InferRequest):
    # If distribute is true, pick a peer and forward (simple round-robin)
    if req.distribute:
        peers = get_peers()
        if not peers:
            # fallback to local run
            pass
        else:
            # choose a peer (round-robin via discovery helper)
            target = discovery.choose_peer()
            if target:
                # forward and return the forwarded response
                body = {"model": req.model, "data": req.data}
                resp = await serving.forward_inference(target, body)
                return InferResponse(model=resp.get("model"), output=resp.get("output"), node=resp.get("node"))

    # local inference
    model = model_zoo.get_model(req.model)
    if model is None:
        raise HTTPException(status_code=404, detail=f"model '{req.model}' not found")
    out = model_zoo.infer(model, req.data)
    return InferResponse(model=req.model, output=out, node=get_node_name())


@router.post("/forward")
async def forward_endpoint(payload: dict, request: Request):
    # This endpoint receives forwarded requests from other nodes
    model_name = payload.get("model")
    data = payload.get("data")
    model = model_zoo.get_model(model_name)
    if model is None:
        raise HTTPException(status_code=404, detail=f"model '{model_name}' not found on target")
    out = model_zoo.infer(model, data)
    return {"model": model_name, "output": out, "node": get_node_name()}
