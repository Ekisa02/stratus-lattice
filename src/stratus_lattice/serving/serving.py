import asyncio
import aiohttp
import json
from typing import Dict, Any
from ..config import get_forward_path


async def forward_inference(peer: str, body: Dict[str, Any], timeout: float = 5.0) -> Dict[str, Any]:
    # peer expected as host[:port]
    scheme = "http"
    url = f"{scheme}://{peer}{get_forward_path()}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=body, timeout=timeout) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise RuntimeError(f"forward failed: {resp.status} {text}")
                return await resp.json()
        except Exception as e:
            # bubble up
            raise
