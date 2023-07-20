import requests
from .endpoints import *
from .models import *


class TrovoClient:
    def __init__(self, client_id: str, access_token: Optional[str] = None):
        self.client_id = client_id
        self.access_token = access_token
        self.headers = {"Accept": "application/json", "Client-ID": self.client_id}
        self.auth = {"Authorization": f"OAuth {self.access_token}"}
        self.headers_with_auth = {**self.headers, **self.auth}

    def __check_access_token(self):
        if self.access_token is None:
            raise ValueError("Access token is required for this operation")

    def __auth_get_request(self, url: str):
        self.__check_access_token()
        r = requests.get(url, headers=self.headers_with_auth)
        return r.json()

    def __auth_get_request_with_params(self, url: str, params: dict):
        self.__check_access_token()
        r = requests.get(url, headers=self.headers_with_auth, params=params)
        return r.json()

    def set_client_id(self, client_id):
        self.client_id = client_id

    def set_access_token(self, access_token):
        self.access_token = access_token

    def process_post_method(self, url, data):
        request = requests.post(url, headers=self.headers, json=data)
        request.raise_for_status()
        response = request.json()

        return response

    def get_game_categories(self) -> GameCategoriesResponse:
        request = requests.get(GAME_CATEGORIES_URL, headers=self.headers)
        request.raise_for_status()
        response = request.json()

        return GameCategoriesResponse(**response)

    def search_game_categories(
        self, query: str, limit: int = 20
    ) -> GameCategoriesResponse:
        data_validation = CategorySearchRequest(query=query, limit=limit)
        data = data_validation.model_dump()
        response = self.process_post_method(SEARCH_CATEGORIES_URL, data)
        return GameCategoriesResponse(**response)

    def get_top_channels(
        self,
        *,
        limit: int = 20,
        after: Optional[bool] = None,
        token: Optional[str] = None,
        cursor: Optional[int] = None,
        category_id: Optional[str] = None,
    ) -> TopChannelsResponse:
        data_validation = TopChannelsRequest(
            limit=limit,
            after=after,
            token=token,
            cursor=cursor,
            category_id=category_id,
        )
        data = data_validation.model_dump(exclude_none=True)
        response = self.process_post_method(TOP_CHANNELS_URL, data)
        return TopChannelsResponse(**response)

    def get_users_by_username(self, users: List[str]):
        data = {"users": users}
        response = self.process_post_method(GET_USERS_URL, data=data)
        return UserSearchResponse(**response)

    def get_channel_info_by_id(
        self, channel_id: Optional[str] = None, username: Optional[str] = None
    ) -> ChannelInfoResponse:
        request_data_validation = ChannelInfoRequest(
            channel_id=channel_id, username=username
        )
        data = request_data_validation.model_dump(exclude_none=True)
        response = self.process_post_method(GET_CHANNEL_INFO_URL, data=data)
        return ChannelInfoResponse(**response)

    # FINISH TESTING
    def get_channel_info_by_streamkey(self):
        response = self.__auth_get_request(READ_CHANNEL_INFO_URL)
        return ChannelStreamKeyResponse(**response)

    def edit_channel_info(
        self,
        channel_id: int,
        live_title: Optional[str] = None,
        category: Optional[str] = None,
        language_code: Optional[str] = None,
        audi_type: Optional[str] = None,
    ):
        data_validation = ChannelEditInfoRequest(
            channel_id=channel_id,
            live_title=live_title,
            category=category,
            language_code=language_code,
            audi_type=audi_type,
        )
        data = data_validation.model_dump(exclude_none=True)
        response = requests.post(
            EDIT_CHANNEL_INTO_URL, headers=self.headers_with_auth, json=data
        )

    def get_user_info(self):
        response = self.__auth_get_request(GET_USER_INFO_URL)
        return UserInfoResponse(**response)

    def get_subscribers(
        self, channel_id: int, limit: int = 25, offset: int = 0, direction: str = "asc"
    ):
        data_validation = GetSubsRequest(
            limit=limit, offset=offset, direction=direction
        )
        url = CHANNEL_URL + f"/{channel_id}/subscriptions"
        data = data_validation.model_dump()
        response = self.__auth_get_request_with_params(url, data)
        return GetSubsResponse(**response)

    def get_emotes(self, emote_type: int, channel_id: List[int]):
        data_validation = GetEmotesRequest(emote_type=emote_type, channel_id=channel_id)
        data = data_validation.model_dump(exclude_none=True)
        response = self.process_post_method(GET_EMOTES_URL, data=data)
        return response

    def get_channel_viewers(self, channel_id: int, limit: int = 20, cursor: int = 0):
        data_validation = GetChannelViewersRequest(limit=limit, cursor=cursor)
        data = data_validation.model_dump()
        url = CHANNEL_URL + f"/{channel_id}/viewers"
        response = self.process_post_method(url, data=data)
        return GetChannelViewersResponse(**response)

    def get_channel_followers(
        self, channel_id: int, limit: int = 20, cursor: int = 0, direction: str = "asc"
    ):
        data_validation = GetChannelFollowersRequest(
            limit=limit, cursor=cursor, direction=direction
        )

        data = data_validation.model_dump()
        url = CHANNEL_URL + f"/{channel_id}/followers"
        response = self.process_post_method(url, data=data)
        return GetChannelFollowersResponse(**response)

    def get_live_stream_urls(self, channel_id: int):
        data = {"channel_id": channel_id}
        headers = self.headers
        headers["Referer"] = "http://openplatform.trovo.live"
        r = requests.post(GET_LIVESTREAMS_URL, headers=headers, json=data)
        return GetLiveStreamsUrlsResponse(**r.json())

    def get_clips_info(
        self,
        channel_id: int,
        category_id: Optional[str] = None,
        period: Optional[str] = "week",
        clip_id: Optional[str] = None,
        limit: Optional[int] = 20,
        cursor: Optional[int] = 0,
        direction: Optional[str] = "asc",
    ):
        data_validation = GetClipsRequest(
            channel_id=channel_id,
            category_id=category_id,
            period=period,
            clip_id=clip_id,
            limit=limit,
            cursor=cursor,
            direction=direction,
        )
        data = data_validation.model_dump(exclude_none=True)
        response = self.process_post_method(GET_CLIPS_INFO_URL, data=data)
        return GetClipsResponse(**response)

    def get_past_streams_info(
        self,
        channel_id: int,
        category_id: Optional[str] = None,
        period: Optional[str] = "week",
        past_stream_id: Optional[str] = None,
        limit: Optional[int] = 20,
        cursor: Optional[int] = 0,
        direction: Optional[str] = "asc",
    ):
        data_validation = GetPastStreamsInfo(
            channel_id=channel_id,
            category_id=category_id,
            period=period,
            past_stream_id=past_stream_id,
            limit=limit,
            cursor=cursor,
            direction=direction,
        )

        data = data_validation.model_dump(exclude_none=True)
        response = self.process_post_method(GET_PAST_STREAMS_URL, data=data)
        return GetPastStreamsResponse(**response)

    def send_chat_to_my_channel(self, content: str):
        data = {"content": content}
        requests.post(CHAT_SEND_URL, headers=self.headers_with_auth, json=data)

    def send_chat_to_selected_channel(self, content: str, channel_id: int):
        data = {"content": content, "channel_id": channel_id}
        requests.post(CHAT_SEND_URL, headers=self.headers_with_auth, json=data)

    def perform_chat_commannd(self, command: str, channel_id: int):
        data = {"command": command, "channel_id": channel_id}
        requests.post(CHAT_COMMAND_URL, headers=self.headers_with_auth, json=data)

    def get_chat_token(self):
        return self.__auth_get_request(GET_CHAT_TOKEN_URL)

    def get_chat_channel_token(self, channel_id: int):
        url = GET_CHAT_CHANNEL_TOKEN_URL + f"/{channel_id}"
        r = requests.get(url, headers=self.headers)
        return r.json()

    # DOUBLE CHECK
    def get_chat_shard_token(self, total_shard: int, current_shard: int):
        data = {"current_shard": current_shard, "total_shard": total_shard}
        url = GET_CHAT_SHARD_TOKEN_URL
        request = requests.get(url, headers=self.headers, params=data)

        response = request.json()
        return response
