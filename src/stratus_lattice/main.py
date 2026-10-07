import os
import uvicorn
from .app import create_app

if __name__ == "__main__":
    host = os.environ.get("STRATUS_HOST", "0.0.0.0")
    port = int(os.environ.get("STRATUS_PORT", "8000"))
    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="info")
