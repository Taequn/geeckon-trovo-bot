import websocket
import json
import threading
import time
import random
import string


class TrovoChat:
    def __init__(self):
        self.token = None

    def generate_nonce(self, length=8):
        """Generate pseudorandom number."""
        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
        )

    def on_message(self, ws, message):
        print("Received: " + message)

    def on_error(self, ws, error):
        print("Error: " + str(error))

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        def run():
            # Authentication
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

    def start_chat(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            "wss://open-chat.trovo.live/chat",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        ws.on_open = self.on_open
        ws.run_forever()
