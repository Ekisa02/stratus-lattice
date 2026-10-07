import random
from ..config import get_peers

# Very small pluggable discovery helper; replace with stronger implementation for prod

_last_choice = -1


def list_peers():
    return get_peers()


def choose_peer() -> str:
    peers = list_peers()
    if not peers:
        return None
    # simple round-robin across peers
    global _last_choice
    _last_choice = (_last_choice + 1) % len(peers)
    return peers[_last_choice]
