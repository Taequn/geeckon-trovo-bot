from pydantic import BaseModel, validator, Field
from typing import List, Optional


class GameCategory(BaseModel):
    id: str
    name: str
    short_name: str
    icon_url: str
    desc: str


class GameCategoriesResponse(BaseModel):
    category_info: List[GameCategory]
    has_more: Optional[bool]


class CategorySearchRequest(BaseModel):
    query: str
    limit: int = Field(20, ge=1, le=100)


class TopChannelsRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100)
    after: Optional[bool]
    token: Optional[str]
    cursor: Optional[int]
    category_id: Optional[str]


class ChannelSocials(BaseModel):
    type: str
    url: str


class BaseChannel(BaseModel):
    is_live: bool
    category_id: str
    category_name: str
    audi_type: str
    language_code: str
    thumbnail: str
    current_viewers: int
    profile_pic: str
    username: str
    subscriber_num: int
    social_links: List[ChannelSocials]


class Channel(BaseChannel):
    channel_id: str
    streamer_user_id: str
    channel_url: str
    title: str
    nick_name: str
    stream_started_at: str
    video_resolution: str
    channel_country: str
    num_followers: int
    


class TopChannelsResponse(BaseModel):
    top_channels_lists: List[Channel]
    total_page: int
    token: str
    cursor: int


class User(BaseModel):
    user_id: str
    username: str
    nickname: str
    channel_id: str


class UserSearchResponse(BaseModel):
    total: int
    users: List[User]


class ChannelInfoResponse(BaseChannel):
    live_title: str
    followers: int
    streamer_info: str
    channel_url: str
    created_at: str
    started_at: str
    ended_at: str

class ChannelInfoRequest(BaseModel):
    channel_id: Optional[str]
    username: Optional[str]

class ChannelStreamKeyResponse(BaseChannel):
    uid: str
    channel_id: str
    stream_key: str
    created_at: str
