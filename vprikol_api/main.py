import time

from .model import IpAPIResponse, MembersAPIResponse, PlayerInfoAPIResponse, CreatedFindTaskAPIResponse, \
    ServerStatusAPIResponse, RatingAPIResponse, CheckRPUsernameAPIResponse, GenerateRPUsernameAPIResponse, \
    PlayerInfoNotFound, PlayerOnlineAPIResponse

from .api import get, post
from typing import Literal
import asyncio
from pydantic import parse_obj_as, ValidationError


class VprikolAPI:
    def __init__(self, token: str, base_url: str = 'https://api.szx.su/'):
        if not token.startswith('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'):
            raise Exception('Токен передан неправильно.')
        self.headers = {'Authorization': f'Bearer {token}'}
        self.base_url = base_url

    async def get_ip_info(self, ip: str) -> IpAPIResponse:
        result = await get(url=f'{self.base_url}ip', headers=self.headers, params={'ip': ip})

        if not result.success:
            raise Exception(result.error)

        return IpAPIResponse(**result.data)

    async def get_members(self, server_id: int, fraction_id: int | list[int]) -> dict[str, MembersAPIResponse]:
        result = await get(url=f'{self.base_url}members', headers=self.headers, params={'server_id': server_id,
                                                                                        'fraction_id': fraction_id})
        if not result.success:
            raise Exception(result.error)
        response = {}
        for fraction_id in result.data:
            players = []
            if not fraction_id.isdigit():
                continue
            for player in result.data[fraction_id]['players']:
                players.append({'username': player, 'id': result.data[fraction_id]['players'][player]['id'],
                                'isOnline': result.data[fraction_id]['players'][player]['isOnline'],
                                'isLeader': result.data[fraction_id]['players'][player]['isLeader'],
                                'rank': result.data[fraction_id]['players'][player]['rank'],
                                'rankLabel': result.data[fraction_id]['players'][player]['rankLabel'],
                                'ingameId': result.data[fraction_id]['players'][player]['ingameId'],
                                'lvl': result.data[fraction_id]['players'][player]['lvl'],
                                'ping': result.data[fraction_id]['players'][player]['ping'],
                                'color': result.data[fraction_id]['players'][player]['color']})
            result.data[fraction_id]['players'] = players
            response[fraction_id] = MembersAPIResponse(**result.data[fraction_id])

        return response

    async def get_player_information(self, server_id: int, nickname: str) -> PlayerInfoAPIResponse | PlayerInfoNotFound:
        task = await post(url=f'{self.base_url}find/createTask', headers=self.headers,
                          params={'server': server_id, 'nick': nickname})
        if not task.success:
            raise Exception(task.error)

        task = CreatedFindTaskAPIResponse(**task.data)
        while True:
            result = await get(url=f'{self.base_url}find/getTaskResult', headers=self.headers,
                               params={'request_id': task.request_id})

            if not result.success and result.error.error_code and result.error.error_code == 425:
                await asyncio.sleep(0.5)
                continue

            if result.error and result.error.error_code == 422:
                return PlayerInfoNotFound(**result.error.dict())

            try:
                return PlayerInfoAPIResponse(**result.data)
            except ValidationError:
                return PlayerInfoAPIResponse(**result.data)

    async def get_server_status(self, server_id: int | None = None) -> list[ServerStatusAPIResponse] | ServerStatusAPIResponse:
        if server_id:
            params = {'server': server_id}
        else:
            params = None

        result = await get(url=f'{self.base_url}status', headers=self.headers,
                           params=params)

        if not result.success:
            raise Exception(result.error)

        if isinstance(result.data, list):
            return parse_obj_as(list[ServerStatusAPIResponse], result.data)

        return ServerStatusAPIResponse(**result.data)

    async def get_rating(self, server_id: int, rating_type: Literal[1, 2, 3]) -> RatingAPIResponse:
        params = {'type': rating_type, 'server': server_id}

        result = await get(url=f'{self.base_url}rating', headers=self.headers,
                           params=params)

        if not result.success:
            raise Exception(result.error)

        return RatingAPIResponse(**result.data)

    async def check_rp_nickname(self, nickname: str, ai: bool = False) -> CheckRPUsernameAPIResponse:
        result = await get(url=f'{self.base_url}checkrp', headers=self.headers,
                           params={'nick': nickname, 'ai': int(ai)})

        if not result.success:
            raise Exception(result.error)
        return CheckRPUsernameAPIResponse(**result.data)

    async def generate_rp_nickname(self, gender: Literal['male', 'female'], nation: Literal[
        'russian', 'american', 'german', 'french', 'italian', 'japanese', 'latinos', 'swedish', 'danish', 'romanian']) \
            -> GenerateRPUsernameAPIResponse:
        result = await get(url=f'{self.base_url}rpnick', headers=self.headers,
                           params={'gender': gender, 'nation': nation})
        if not result.success:
            raise Exception(result.error)

        return GenerateRPUsernameAPIResponse(**result.data)

    async def get_player_online(self, nickname: str, server_id: int, count: int = 100,
                                offset: int = 0, date: int = int(time.time())) -> PlayerOnlineAPIResponse:
        result = await get(url=f'{self.base_url}online', headers=self.headers,
                           params={'nickname': nickname, 'count': count, 'offset': offset, 'server_id': server_id,
                                   'filter_by_date': date})

        if not result.success:
            raise Exception(result.error)

        return PlayerOnlineAPIResponse(**result.data)
