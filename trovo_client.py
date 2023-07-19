import requests
import os
from dotenv import load_dotenv
import webbrowser

load_dotenv()


CLIENT_ID = os.environ["CLIENT_ID"]
scopes_list = [
    "send_to_my_channel",
    "chat_send_self",
    "manage_messages",
    "channel_subscriptions",
]
scopes = "+".join(scopes_list)
redirect_uri = "http://127.0.0.1"


# Construct the authorization URL
auth_url = f"https://open.trovo.live/page/login.html?client_id={CLIENT_ID}&response_type=token&scope={scopes}&redirect_uri={redirect_uri}"

# Open the URL in a web browser
webbrowser.open(auth_url)
