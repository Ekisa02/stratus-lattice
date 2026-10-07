import os
from typing import List


def get_node_name() -> str:
    return os.environ.get("STRATUS_NODE_NAME", "node-unknown")


def get_peers() -> List[str]:
    # STRATUS_PEERS is a comma-separated list of host:port
    raw = os.environ.get("STRATUS_PEERS", "")
    if not raw:
        return []
    peers = [p.strip() for p in raw.split(",") if p.strip()]
    return peers


def get_forward_path() -> str:
    return os.environ.get("STRATUS_FORWARD_PATH", "/forward")
