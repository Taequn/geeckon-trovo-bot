import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.client_id = os.environ['CLIENT_ID']
        self.secret = os.environ['SECRET']
        self.oauth = os.environ['OAUTH']
        self.lambda_link = os.environ['LAMBDA']

congif = Config()