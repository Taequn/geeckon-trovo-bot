import requests
from trovo.core.config import congif

def get_all_the_users_for_community(community_id: str):
    main_url = congif.lambda_link
    url = main_url + 'api/v1/communities/{community_id}/users'
    r = requests.get(url)
    print(r.text)
    
if __name__ == "__main__":
    get_all_the_users_for_community('b4435b80-d72a-43e4-b296-0561eeacfd43')