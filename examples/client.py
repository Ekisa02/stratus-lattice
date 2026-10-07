import asyncio
import httpx


async def main():
    # Example: call a node, request distributed inference
    async with httpx.AsyncClient() as client:
        # load a tiny model
        resp = await client.post("http://127.0.0.1:8000/load_model", json={"name":"tiny","input_dim":8})
        print("load_model:", resp.json())

        # local inference
        payload = {"model": "tiny", "data": [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8], "distribute": False}
        r = await client.post("http://127.0.0.1:8000/infer", json=payload)
        print("infer-local:", r.json())

        # distributed (forward to peer if configured)
        payload["distribute"] = True
        r2 = await client.post("http://127.0.0.1:8000/infer", json=payload)
        print("infer-distributed:", r2.json())


if __name__ == "__main__":
    asyncio.run(main())
