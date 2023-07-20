from trovo.client.trovo_client import TrovoClient

class CommandHandler:
    def __init__(self, trovo_client: TrovoClient, channel_id: int):
        self.trovo = trovo_client
        self.channel_id = channel_id
        self.commands = {
            "!help": self.help_command,
            "!hello": self.hello_command,
        }

    def send_message(self, message):
        self.trovo.send_chat_to_selected_channel(message, self.channel_id)
    
    def help_command(self, username: str):
        message = f"The help will be here shortly, {username}"
        self.send_message(message)

    def hello_command(self, username: str):
        message = f'Hello there, @{username}!'
        self.send_message(message)

    def select_command(self, username: str, message: str):
        if message.startswith("!"):
            words = message.split()
            command_to_execute = words[0]
            if command_to_execute in self.commands:
                self.commands[command_to_execute](username)
