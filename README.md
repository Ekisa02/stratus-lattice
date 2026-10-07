# Stratus Lattice

Stratus Lattice is a lightweight distributed cloud systems framework for model serving and orchestration. It provides a FastAPI-based HTTP service that loads PyTorch models, exposes inference endpoints, and can forward or balance inference requests across peer nodes (a "lattice") for horizontal scaling.

This repository is intended as a reference architecture and a starting point for production systems: modular components for discovery, serving, model management, and integration testing.

Key Features
- FastAPI-driven HTTP API for serving and orchestration.
- PyTorch models with a small model zoo and simple save/load utilities.
- Pluggable peer discovery (env/config-driven), and HTTP forwarding for distributed inference.
- Async-friendly, testable code with example client usage and docker-compose for local multi-node simulation.

Repository layout

- src/stratus_lattice/
  - app.py             # FastAPI application factory
  - main.py            # CLI entrypoint (uvicorn)
  - config.py          # runtime configuration and environment parsing
  - models/            # model zoo and save/load helpers
  - serving/           # main serving logic and forwarding client
  - discovery/         # peer discovery helpers
  - api/               # pydantic schemas and API routers
  - tasks/             # simple in-process task queue (pluggable)
  - utils/             # logging and helpers
- tests/               # pytest tests
- examples/            # example client usage
- docker-compose.yml   # sample local composition to run a few nodes
- Dockerfile           # container definition
- requirements.txt


Architecture (high level)

1) HTTP API (FastAPI)
   - /infer: Accepts a payload and either runs local inference or forwards to peers.
   - /load_model: Loads a named model into the node's model registry.
   - /peers: Returns known peers.

2) Discovery
   - Simple environment-configured peer list for local/dev. Pluggable to replace with etcd/consul/Redis/k8s.

3) Forwarding / Distribution
   - Outgoing requests to peers use aiohttp to forward JSON requests to /forward endpoints.
   - Basic round-robin selection; configurable to use topology-aware routing.

4) Model Management
   - In-memory model registry with simple save/load utilities.
   - Models built with PyTorch—CPU by default.

5) Extensibility
   - Queue abstraction (in-memory/Redis), pluggable discovery, metrics hooks, authentication layers.


Quickstart (Local, single-node)

1. Create a virtualenv and install dependencies

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run the app

   export STRATUS_NODE_NAME=node-1
   export STRATUS_PEERS=
   python -m src.stratus_lattice.main

3. Load a model and run inference (example)

   # load a small random model
   curl -X POST "http://127.0.0.1:8000/load_model" -H "Content-Type: application/json" -d '{"name":"tiny","input_dim":8}
'

   # infer
   curl -X POST "http://127.0.0.1:8000/infer" -H "Content-Type: application/json" -d '{"model":"tiny","data":[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]}'


Distributed demo (local multi-node using docker-compose)

- Use docker-compose to spin up 2+ nodes and an optional Redis for queueing. The compose file maps STRATUS_PEERS so nodes know each other.


Testing

Run pytest:

    pytest -q


Extending

- Replace discovery with a k8s API poll for service endpoints.
- Add authentication to endpoints (JWT/mTLS).
- Integrate a production queue like Redis/RabbitMQ.
- Add metrics (Prometheus) and tracing (OpenTelemetry).


License

MIT
