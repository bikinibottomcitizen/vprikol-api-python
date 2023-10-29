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
    ingame_id: int | None = Field(alias='ingameId')
    ping: int | None
    lvl: int | None
    color: int | None


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
    online_updated_at: int = Field(alias='updated_at_online')


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


class PlayerInfoAPIResponse(BaseModel):
    account_id: int | None = Field(alias='accountId')
    player_id: int | None = Field(alias='playerId')
    lvl: int | None
    cash: int | None
    bank: int | None
    individual_account: int | None = Field(alias='individualAccount')
    deposit: int | None
    total_money: int | None = Field(alias='totalMoney')
    is_online: bool = Field(alias='isOnline')
    job_label: str | None = Field(alias='jobLabel')
    job_id: int | None = Field(alias='jobId')
    rank_number: int | None = Field(alias='rankNumber')
    rank_label: str | None = Field(alias='rankLabel')
    is_leader: bool = Field(alias='isLeader')
    org_label: str = Field(alias='orgLabel')
    org_id: int = Field(alias='orgId')
    vip_lvl: int | None = Field(alias='vipLvl')
    vip_label: str | None = Field(alias='vipLabel')
    phone_number: int | None = Field(alias='phoneNumber')
    updated_at: int = Field(alias='updatedAt')
    player_nick: str = Field(alias='playerNick')
    player_server: int = Field(alias='playerServer')
    server_name: str = Field(alias='serverName')


class PlayerInfoNotFound(APIErrorResponse):
    pass


class RatingPlayerInfo(BaseModel):
    number: int
    name: str
    is_online: bool = Field('isOnline')


class RatingAPIResponse(BaseModel):
    server: str
    players: list[RatingPlayerInfo]


class IpAPIResponse(BaseModel):
    ip: str
    country: str
    city: str
    timezone: str
    isp: str


class CheckRPUsernameName(BaseModel):
    rp: bool
    graph: str | None
    gpt_answer: str | None


class CheckRPUsernameAPIResponse(BaseModel):
    name: CheckRPUsernameName
    surname: CheckRPUsernameName
    nickname: str = Field(alias='nick')


class GenerateRPUsernameAPIResponse(BaseModel):
    name: str
    surname: str
