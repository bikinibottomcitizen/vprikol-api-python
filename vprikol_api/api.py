import aiohttp
import json
from .model import Response


async def get(url: str, params: dict | None = None, headers: dict | None = None) -> Response:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params) as response:
            response_json = json.loads(await response.text())
            if response.ok:
                return Response(data=response_json)
            return Response(error=response_json, success=False)


async def post(url: str, params: dict | None = None, headers: dict | None = None) -> Response:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, params=params) as response:
            response_json = json.loads(await response.text())
            if response.ok:
                return Response(data=response_json)
            return Response(error=response_json, success=False)
