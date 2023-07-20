from pydantic import BaseModel, validator, Field
from typing import List, Optional, Dict
import warnings


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
    limit: int = Field(default=20, ge=1, le=100)


class TopChannelsRequest(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
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


class ChannelEditInfoRequest(BaseModel):
    channel_id: int
    live_title: Optional[str] = None
    category: Optional[str] = None
    language_code: Optional[str] = None
    audi_type: Optional[str] = None

    @validator("audi_type")
    def check_audi_type(cls, v):
        if v is not None and v not in [
            "CHANNEL_AUDIENCE_TYPE_FAMILYFRIENDLY",
            "CHANNEL_AUDIENCE_TYPE_TEEN",
            "CHANNEL_AUDIENCE_TYPE_EIGHTEENPLUS",
        ]:
            raise ValueError("Incorrect audi_type: ", v)
        return v

    @validator("language_code")
    def check_language_code(cls, v):
        if v is not None and len(v) != 2:
            raise ValueError("Incorrect country language code: ", v)
        warnings.warn("The language_code does not work properly!")
        return v


class UserInfoResponse(BaseModel):
    userId: str
    userName: str
    nickName: str
    email: str
    profilePic: str
    info: str
    channelId: int


class UserSub(BaseModel):
    user_id: str
    username: str
    display_name: str
    profile_pic: str
    created_at: str


class SubList(BaseModel):
    user: UserSub
    sub_created_at: int
    sub_lv: str
    sub_tier: str


class GetSubsResponse(BaseModel):
    total: int
    subscriptions: List[SubList]


class GetSubsRequest(BaseModel):
    limit: int = Field(default=25, ge=0, le=100)
    offset: int = Field(default=0, ge=0)
    direction: str = "asc"

    @validator("direction")
    def check_direction_variable(cls, v):
        if v not in ["asc", "desc"]:
            raise ValueError(
                "Incorrect value for direction: it can only be 'asc' or 'desc', provided value: ",
                v,
            )
        return v


class GetEmotesRequest(BaseModel):
    emote_type: int
    channel_id: List[int]

    @validator("emote_type")
    def check_emote_type(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError(
                "Incorrect value for emote_type: it can only be 0/1/2, provided value: ",
                v,
            )
        return v


class GetChannelViewersRequest(BaseModel):
    limit: Optional[int] = Field(default=20, ge=20, le=200)
    cursor: Optional[int] = Field(default=0, ge=0)


class Viewers(BaseModel):
    viewers: List[str]


class Chatters(BaseModel):
    VIPS: Viewers
    ace: Viewers
    aceplus: Viewers
    admins: Viewers
    all: Viewers
    creators: Viewers
    editors: Viewers
    followers: Viewers
    moderators: Viewers
    subscribers: Viewers
    supermods: Viewers
    wardens: Viewers


class GetChannelViewersResponse(BaseModel):
    live_title: str
    total: str
    nickname: str
    chatters: Chatters
    custome_roles: Dict[str, Viewers]

    class Config:
        extra = "allow"


class GetChannelFollowersRequest(GetChannelViewersRequest):
    direction: str = "asc"

    @validator("direction")
    def check_direction(cls, v):
        if v not in ["asc", "desc"]:
            raise ValueError(
                "Incorrect value for direction: it can only be 'asc' or 'desc', provided value: ",
                v,
            )
        return v


class ChannelFollower(BaseModel):
    user_id: str
    nickname: str
    profile_pic: str
    followed_at: str


class GetChannelFollowersResponse(BaseModel):
    total: str
    follower: List[ChannelFollower]
    total_page: int
    cursor: int


class StreamUrls(BaseModel):
    play_url: Optional[str]
    desc: Optional[str]


class GetLiveStreamsUrlsResponse(BaseModel):
    stream_urls: List[StreamUrls]


class GetClipsRequest(BaseModel):
    channel_id: int
    category_id: Optional[str] = None
    period: Optional[str] = "week"
    clip_id: Optional[str] = None
    limit: Optional[int] = Field(default=20, ge=0, le=100)
    cursor: Optional[int] = Field(default=0, ge=0)
    direction: Optional[str] = "asc"

    @validator("direction")
    def check_direction(cls, v):
        if v not in ["asc", "desc"]:
            raise ValueError(
                "Incorrect value for direction: it can only be 'asc' or 'desc', provided value: ",
                v,
            )
        return v

    @validator("period")
    def check_period(cls, v):
        if v not in ["day", "week", "month", "all"]:
            raise ValueError(
                "Incorrect value for period: it can only be day/week/month/all, provided value: ",
                v,
            )


class ClipInfo(BaseModel):
    streamer_id: str
    streamer_username: str
    streamer_nickname: str
    clip_id: str
    title: str
    url: str
    language: str
    thumbnail: str
    category_id: str
    sub_only: bool
    made_at: str
    duration: int
    views: int
    likes: int
    comments_number: int
    maker_username: str
    maker_nickname: str


class GetClipsResponse(BaseModel):
    total_clips: int
    clips_info: List[ClipInfo]
    total_page: int
    cursor: int


class GetPastStreamsInfo(GetClipsRequest):
    past_stream_id: Optional[str] = None


class PastStreamInfo(BaseModel):
    streamer_id: str
    streamer_username: str
    streamer_nickname: str
    past_stream_id: str
    title: str
    url: str
    language: str
    thumbnail: str
    category_id: str
    sub_only: bool
    duration: int
    start_at: str
    end_at: str
    views: int
    likes: int
    comments_number: int


class GetPastStreamsResponse(BaseModel):
    total_past_streams: int
    past_streams_info: List[PastStreamInfo]
    total_page: int
    cursor: int
