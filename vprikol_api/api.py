from typing import Optional, Dict

import aiohttp

from .model import Response


async def get_json(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Response:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params) as response:
            response_json = await response.json()
            if response.ok:
                return Response(data=response_json)
            return Response(error=response_json, success=False)


async def post_json(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Response:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, params=params) as response:
            response_json = await response.json()
            if response.ok:
                return Response(data=response_json)
            return Response(error=response_json, success=False)


async def get_bytes(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Response:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params) as response:
            response_data = await response.read()
            if response.status == 200:
                return Response(data=response_data)
            return Response(error=(await response.json()), success=False)
