from typing import TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class FastAPIErrorDetail(BaseModel):
    loc: list[str]
    message: str = Field(alias='msg')
    type: str


class FastApiErrorResponse(BaseModel):
    detail: FastAPIErrorDetail | str


class APIErrorResponse(BaseModel):
    error_code: int
    detail: str
    queue_position: int | None = None


class Response(GenericModel):
    data: DataT | None
    error: APIErrorResponse | FastApiErrorResponse | None
    success: bool = True


class MembersAPIPlayer(BaseModel):
    username: str
    id: int | None
    is_online: bool = Field(alias='isOnline')
    is_leader: bool = Field(alias='isLeader')
    rank: int
    rank_label: str | None = Field(alias='rankLabel')
    ingame_id: int = Field(alias='ingameId')
    ping: int
    lvl: int
    color: int


class MembersAPIRecord(BaseModel):
    count: int
    date: str
    leader: str


class MembersAPIResponse(BaseModel):
    server_label: str = Field(alias='serverName')
    fraction_label: str = Field(alias='fractionLabel')
    players: list[MembersAPIPlayer]
    record: MembersAPIRecord
    total_players: int = Field(alias='totalPlayers')
    total_online: int = Field(alias='totalOnline')
    leader_nickname: str | None = Field(alias='leaderNick')
    is_leader_online: bool = Field(alias='isLeaderOnline')


class ServerStatusAPIResponse(BaseModel):
    server_number: int = Field(alias='number')
    ip: str
    port: int
    online_players: int = Field(alias='onlinePlayers')
    max_players: int = Field(alias='maxPlayers')
    is_closed: bool = Field(alias='isClosed')
    server_label: str = Field(alias='serverLabel')


class CreatedFindTaskAPIResponse(BaseModel):
    request_id: str
    request_time: int
    queue_position: int


class PlayerInfoArizonaAPIResponse(BaseModel):
    account_id: int = Field(alias='accountId')
    player_id: int | None = Field(alias='playerId')
    lvl: int
    cash: int
    bank: int
    individual_account: int | None = Field(alias='individualAccount')
    deposit: int
    total_money: int = Field(alias='totalMoney')
    is_online: bool = Field(alias='isOnline')
    job_label: str = Field(alias='jobLabel')
    job_id: int = Field(alias='jobId')
    rank_number: int | None = Field(alias='rankNumber')
    rank_label: str | None = Field(alias='rankLabel')
    is_leader: bool = Field(alias='isLeader')
    org_label: str = Field(alias='orgLabel')
    org_id: int = Field(alias='orgId')
    vip_lvl: int = Field(alias='vipLvl')
    vip_label: str = Field(alias='vipLabel')
    phone_number: int | None = Field(alias='phoneNumber')
    updated_at: int = Field(alias='updatedAt')
    player_nick: str = Field(alias='playerNick')
    player_server: int = Field(alias='playerServer')
    server_name: str = Field(alias='serverName')


class PlayerInfoNotFound(APIErrorResponse):
    pass


class PlayerInfoRodinaAPIResponse(BaseModel):
    hp: int
    hunger: int
    lvl: int
    vip: str
    cash: int
    bank: int
    azCoins: int
    isLeader: bool
    fraction: str
    rank: int
    job: str
    isOnline: bool


class RatingPlayerAPI(BaseModel):
    number: int
    name: str
    is_online: bool = Field('isOnline')


class RatingFamilyAPI(BaseModel):
    number: int
    name: str
    owner: str
    lvl: int


class RatingAPIResponse(BaseModel):
    server: str
    players: list[RatingPlayerAPI] | None
    families: list[RatingFamilyAPI] | None


class IpAPIResponse(BaseModel):
    ip: str
    country: str
    city: str
    timezone: str
    isp: str


class CheckRPUsernameName(BaseModel):
    rp: bool
    schedule: str | None


class CheckRPUsernameAPIResponse(BaseModel):
    name: CheckRPUsernameName
    surname: CheckRPUsernameName
    nickname: str = Field(alias='nick')


class GenerateRPUsernameAPIResponse(BaseModel):
    name: str
    surname: str
