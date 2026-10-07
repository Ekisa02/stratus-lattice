from fastapi import FastAPI
from .api import router as api_router
from .utils.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="Stratus Lattice")
    app.include_router(api_router)
    return app
