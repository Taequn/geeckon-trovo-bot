import websocket
import json
import threading
import time
import random
import string
from trovo.client.trovo_client import TrovoClient
from trovo.chat.command_handler import CommandHandler
from trovo.chat.helper_functions import extract_message_type_contents

class TrovoChat:
    def __init__(self, client_id: str, access_token: str, channel_id: int):
        self.token = None
        self.channel_id = channel_id
        self.trovo = TrovoClient(client_id=client_id, access_token=access_token)
        self.handler = CommandHandler(self.trovo, self.channel_id)

    def generate_chat_token(self):
        response = self.trovo.get_chat_channel_token(self.channel_id)
        self.token = response["token"]

    def generate_nonce(self, length: int = 8):
        """Generate pseudorandom number."""
        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
        )

    def on_message(self, ws, message):
        print(message)
        try:
            username, content = extract_message_type_contents(message)  # type: ignore
            print(username, content)
            self.handler.select_command(username, content)
        except Exception as e:
            pass

    def on_error(self, ws, error):
        print("Error: " + str(error))

    def on_close(self, ws):
        print("### Connection closed ###")

    def on_open(self, ws):
        def run():
            # Authentication
            self.generate_chat_token()
            auth_data = {
                "type": "AUTH",
                "nonce": self.generate_nonce(),
                "data": {"token": self.token},
            }
            ws.send(json.dumps(auth_data))

            # Keeping connection alive
            while True:
                time.sleep(30)
                ping_data = {"type": "PING", "nonce": self.generate_nonce()}
                ws.send(json.dumps(ping_data))

        threading.Thread(target=run).start()

    def run_forever(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            "wss://open-chat.trovo.live/chat",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        ws.on_open = self.on_open
        ws.run_forever()
