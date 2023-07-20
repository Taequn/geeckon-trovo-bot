import json


def extract_message_type_contents(raw_message: str):
    try:
        message = json.loads(raw_message)
        if message.get("type") == "CHAT" and message.get("channel_info") is not None:
            chats = message.get("data").get("chats")
            username = chats[0]["nick_name"]
            content = chats[0]["content"]

            return username, content
    except json.JSONDecodeError as e:
        return None
