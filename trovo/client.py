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
        request_data_validation = ChannelInfoRequest(channel_id=channel_id, username=username)
        data = request_data_validation.model_dump(exclude_none=True)
        
        response = self.process_post_method(GET_CHANNEL_INFO_URL, data=data)
        
        channel_info = ChannelInfoResponse(**response)
        return channel_info

    # FINISH TESTING
    def get_channel_info_by_streamkey(self):
        if self.access_token is None:
            raise ValueError("Access token is required for this operation")
        
        headers = self.headers
        headers['Authorization'] = f'OAuth {self.access_token}'
        
        request = requests.get(READ_CHANNEL_INFO_URL, 
                               headers=headers)
        
        response = request.json()
        
        channel_info = ChannelStreamKeyResponse(**response)
        return response
    
    
        
