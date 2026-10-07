# Stratus Lattice Architecture

This document outlines the reference architecture used by Stratus Lattice:

1. API Layer (FastAPI)
   - Responsible for accepting HTTP requests from clients or other nodes.
   - Exposes endpoints: /infer, /load_model, /peers, /forward.

2. Discovery
   - Lightweight discovery for local/dev uses environment variables.
   - Hook points exist for service discovery via consistent registries (Consul, etcd), k8s API, or DNS.

3. Model Registry
   - In-memory registry for loaded models. For multi-node consistency, models can be saved to shared object storage or pushed to peers.

4. Forwarder
   - Uses aiohttp for non-blocking HTTP forwarding. Could be extended to gRPC for better efficiency.

5. Task Queue
   - Optional queue abstraction to shuttle heavy inference jobs off request threads; can be plugged into Redis/Celery.

6. Observability
   - Adding Prometheus metrics, structured logs, and tracing is straightforward via middleware.
