from typing import TypeVar, List, Optional, Dict, Generic, Union

from pydantic import BaseModel, Field

DataT = TypeVar('DataT')


class FastAPIErrorDetail(BaseModel):
    loc: List[str]
    message: str = Field(alias='msg')
    type: str


class FastApiErrorResponse(BaseModel):
    detail: Union[FastAPIErrorDetail, str]


class APIErrorResponse(BaseModel):
    error_code: int
    detail: str
    queue_position: Optional[int] = None


class Response(BaseModel, Generic[DataT]):
    data: Optional[DataT] = None
    error: Optional[Union[FastApiErrorResponse, APIErrorResponse]] = None
    success: bool = True


class MembersAPIPlayer(BaseModel):
    username: str
    id: Optional[int] = None
    is_online: bool = Field(alias='isOnline')
    is_leader: bool = Field(alias='isLeader')
    rank: int
    rank_label: Optional[str] = Field(None, alias='rankLabel')
    ingame_id: Optional[int] = Field(None, alias='ingameId')
    ping: Optional[int]
    lvl: Optional[int]
    color: Optional[int]


class MembersAPIRecord(BaseModel):
    count: int
    date: str
    leader: str


class MembersAPIResponse(BaseModel):
    server_label: str = Field(alias='serverName')
    fraction_label: str = Field(alias='fractionLabel')
    players: List[MembersAPIPlayer]
    record: MembersAPIRecord
    total_players: int = Field(alias='totalPlayers')
    total_online: int = Field(alias='totalOnline')
    leader_nickname: Optional[str] = Field(None, alias='leaderNick')
    is_leader_online: bool = Field(alias='isLeaderOnline')
    online_updated_at: int = Field(alias='onlineUpdatedAt')
    members_updated_at: int = Field(alias='membersUpdatedAt')


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
    account_id: Optional[int] = Field(None, alias='accountId')
    player_id: Optional[int] = Field(None, alias='playerId')
    lvl: Optional[int] = None
    cash: Optional[int] = None
    bank: Optional[int] = None
    individual_account: Optional[int] = Field(None, alias='individualAccount')
    deposit: Optional[int] = None
    total_money: Optional[int] = Field(None, alias='totalMoney')
    is_online: bool = Field(False, alias='isOnline')
    job_label: Optional[str] = Field(None, alias='jobLabel')
    job_id: Optional[int] = Field(None, alias='jobId')
    rank_number: Optional[int] = Field(None, alias='rankNumber')
    rank_label: Optional[str] = Field(None, alias='rankLabel')
    is_leader: bool = Field(False, alias='isLeader')
    org_label: str = Field('', alias='orgLabel')
    org_id: int = Field(0, alias='orgId')
    vip_lvl: Optional[int] = Field(None, alias='vipLvl')
    vip_label: Optional[str] = Field(None, alias='vipLabel')
    phone_number: Optional[int] = Field(None, alias='phoneNumber')
    updated_at: int = Field(0, alias='updatedAt')
    player_nick: str = Field('', alias='playerNick')
    player_server: int = Field(0, alias='playerServer')
    server_name: str = Field('', alias='serverName')


class PlayerInfoNotFound(APIErrorResponse):
    pass


class RatingPlayerInfo(BaseModel):
    number: int
    name: str
    is_online: bool = Field('isOnline')


class RatingAPIResponse(BaseModel):
    server: str
    players: List[RatingPlayerInfo]


class IpAPIResponse(BaseModel):
    ip: str
    country: str
    city: str
    timezone: str
    isp: str


class CheckRPUsernameName(BaseModel):
    rp: bool
    graph: Optional[str] = None
    gpt_answer: Optional[str] = None


class CheckRPUsernameAPIResponse(BaseModel):
    name: CheckRPUsernameName
    surname: CheckRPUsernameName
    nickname: str = Field(alias='nick')


class GhettoZonesData(BaseModel):
    grove: int = Field(alias='2569507584')
    ballas: int = Field(alias='2580283596')
    vagos: int = Field(alias='2568805329')
    rifa: int = Field(alias='2583651942')
    aztec: int = Field(alias='2581790464')
    nw: int = Field(alias='2155378856')


class GhettoZonesAPIResponse(BaseModel):
    data: GhettoZonesData
    server_name: str = Field(alias='serverName')
    updated_at: int = Field(alias='updatedAt')


class AuctionInfo(BaseModel):
    active: bool
    minimal_bet: int = Field("minimalBet")
    time_end: int = Field(alias='timeEnd')
    start_price: int = Field(alias='startPrice')


class Coordinates(BaseModel):
    x: float
    y: float


class EstateItem(BaseModel):
    id: int
    name: Optional[str]
    owner: Optional[str]
    auction: AuctionInfo
    coordinates: Coordinates


class PlayerEstateAPIResponse(BaseModel):
    server_id: int = Field(alias='serverId')
    server_label: str = Field(alias='serverLabel')
    nickname: str = Field(alias='nickname')
    houses: List[EstateItem]
    businesses: List[EstateItem]


class GenerateRPUsernameAPIResponse(BaseModel):
    name: str
    surname: str


class OnlinePlayerInfo(BaseModel):
    login_at: int
    logout_at: int


class PlayerOnlineAPIResponse(BaseModel):
    sessions: List[OnlinePlayerInfo]


class PlayerData(BaseModel):
    ingame_id: Optional[int] = Field(None, alias='ingameId')
    lvl: Optional[int] = None
    ping: Optional[int] = None
    color: Optional[int] = None


class PlayersAPIResponse(BaseModel):
    server_name: str = Field(alias='serverName')
    updated_at: int = Field(alias='updatedAt')
    data: Dict[str, Optional[PlayerData]]
