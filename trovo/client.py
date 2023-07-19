import requests
from .endpoints import *
from .models import *


class TrovoClient:
    def __init__(self, client_id, access_token=None):
        self.client_id = client_id
        self.access_token = access_token
        self.headers = {"Accept": "application/json", "Client-ID": self.client_id}

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
        top_categories = GameCategoriesResponse(**response)

        return top_categories

    def search_game_categories(
        self, query: str, limit: int = 20
    ) -> GameCategoriesResponse:
        search_data_validation = CategorySearchRequest(query=query, limit=limit)
        search_data = search_data_validation.model_dump()

        response = self.process_post_method(SEARCH_CATEGORIES_URL, search_data)

        categories = GameCategoriesResponse(**response)
        return categories

    def get_top_channels(
        self,
        *,
        limit: int = 20,
        after: Optional[bool] = None,
        token: Optional[str] = None,
        cursor: Optional[int] = None,
        category_id: Optional[str] = None,
    ) -> TopChannelsResponse:
        channels_data_validation = TopChannelsRequest(
            limit=limit,
            after=after,
            token=token,
            cursor=cursor,
            category_id=category_id,
        )
        channel_request = channels_data_validation.model_dump(exclude_none=True)

        response = self.process_post_method(TOP_CHANNELS_URL, channel_request)

        top_channels = TopChannelsResponse(**response)
        return top_channels

    def get_users_by_username(self, users: List[str]):
        user_data = {"users": users}

        response = self.process_post_method(GET_USERS_URL, data=user_data)

        user_search = UserSearchResponse(**response)
        return user_search

    def get_channel_info_by_id(
        self, channel_id: Optional[str] = None, username: Optional[str] = None
    ) -> ChannelInfoResponse:
        request_data_validation = ChannelInfoRequest(
            channel_id=channel_id, username=username
        )
        data = request_data_validation.model_dump(exclude_none=True)

        response = self.process_post_method(GET_CHANNEL_INFO_URL, data=data)

        channel_info = ChannelInfoResponse(**response)
        return channel_info

    # FINISH TESTING
    def get_channel_info_by_streamkey(self):
        if self.access_token is None:
            raise ValueError("Access token is required for this operation")

        headers = self.headers
        headers["Authorization"] = f"OAuth {self.access_token}"

        request = requests.get(READ_CHANNEL_INFO_URL, headers=headers)

        response = request.json()

        channel_info = ChannelStreamKeyResponse(**response)
        return response

    def edit_channel_info(
        self,
        channel_id: str,
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

        response = self.process_post_method(EDIT_CHANNEL_INTO_URL, data=data)

        return response.json()

    def get_user_info(self):
        headers = self.headers
        headers["Authorization"] = f"Oauth {self.access_token}"
        request = requests.get(GET_USER_INFO_URL, headers=headers)
        response = request.json()

        user_info = UserInfoResponse(**response)
        return user_info

    def get_subscribers(
        self, channel_id: str, limit: int = 25, offset: int = 0, direction: str = "asc"
    ):
        headers = self.headers
        headers["Authorization"] = f"OAuth {self.access_token}"

        url = (
            CHANNEL_URL
            + f"/{channel_id}/subscriptions?limit={limit}&offset={offset}&direction={direction}"
        )
        request = requests.get(url)

        response = request.json()

        sub_list = GetSubsResponse(**response)
        return sub_list

    def get_emotes(self, emote_type: int, channel_id: List[int]):
        data = {"emote_type": emote_type, "channel_id": channel_id}

        response = self.process_post_method(GET_EMOTES_URL, data=data)

        return response

    def get_channel_viewers(self, channel_id: int, limit: int = 20, cursor: int = 0):
        data = {"limit": limit, "cursor": cursor}

        url = CHANNEL_URL + f"/{channel_id}/viewers"
        response = self.process_post_method(url, data=data)

        return response

    def get_channel_followers(
        self, channel_id: int, limit: int = 20, cursor: int = 0, direction: str = "asc"
    ):
        data = {"limit": limit, "cursor": cursor, "direction": direction}

        url = CHANNEL_URL + f"/{channel_id}/followers"
        response = self.process_post_method(url, data=data)

        return response

    def get_live_stream_urls(self, channel_id: int):
        data = {"channel_id": channel_id}

        response = self.process_post_method(GET_LIVESTREAMS_URL, data=data)

        return response

    def get_clips_info(
        self,
        *,
        channel_id: int,
        category_id: str,
        period: str = "week",
        clip_id: str,
        limit: int = 20,
        cursor: int = 0,
        direction: str = "asc",
    ):
        data = {
            "channel_id": channel_id,
            "category_id": category_id,
            "period": period,
            "clip_id": clip_id,
            "limit": limit,
            "cursor": cursor,
            "direction": direction,
        }

        response = self.process_post_method(GET_CLIPS_INFO_URL, data=data)

        return response

    def get_past_streams_info(
        self,
        *,
        channel_id: int,
        category_id: str,
        period: str = "week",
        past_stream_id: str,
        limit: int = 20,
        cursor: int = 0,
        direction: str = "asc",
    ):
        data = {
            "channel_id": channel_id,
            "category_id": category_id,
            "period": period,
            "past_stream_id": past_stream_id,
            "limit": limit,
            "cursor": cursor,
            "direction": direction,
        }

        response = self.process_post_method(GET_PAST_STREAMS_URL, data=data)

        return response

    def send_chat_to_my_channel(self,
                                content: str):
        headers = self.headers
        headers['Authorization'] = f'OAuth {self.access_token}'
        
        data = {
            'content': content
        }
        
        requests.post(CHAT_SEND_URL, json=data)
    
    def send_chat_to_selected_channel(self,
                                      content: str,
                                      channel_id: int):
        headers = self.headers
        headers['Authorization'] = f'OAuth {self.access_token}'
        
        data = {
            'content': content,
            'channel_id': channel_id
        }
        
        requests.post(CHAT_SEND_URL, json=data)
    
    def perform_chat_commannd(self, command: str, channel_id: int):
        headers = self.headers
        headers['Authorization'] = f'OAuth {self.access_token}'
        
        data = {
            'command': command,
            'channel_id': channel_id
        }
        
        requests.post(CHAT_COMMAND_URL, json=data)
    
    def get_chat_token(self):
        headers = self.headers
        headers['Authorization'] = f'OAuth {self.access_token}'
        
        request = requests.get(GET_CHAT_TOKEN_URL, headers=headers)
        
        response = request.json()
        
        return response

    def get_chat_channel_token(self, channel_id: int):
        url = GET_CHAT_CHANNEL_TOKEN_URL + f'/{channel_id}'
        r = requests.get(url, headers=self.headers)
        return r.json()
    
    def get_chat_shard_token(self, total_shard: int, current_shard: int):
        
        data = {
            'current_shard': current_shard,
            'total_shard': total_shard
        }
        
        url = GET_CHAT_SHARD_TOKEN_URL
        print(self.headers)
        request = requests.get(url, headers=self.headers, params=data)
        
        response = request.json()
        return response

    
    
        
