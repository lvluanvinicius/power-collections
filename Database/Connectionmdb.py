from pymongo import MongoClient
from Config.env import EnvConfig
from os import getenv
from sys import path

# Configure path.
path.insert(0, "../")

# Carregando variáveis de ambiente.
EnvConfig().load_env()


class MongoConnection (object):

    def __init__(self):
        self.USERNAME = getenv("MONGODB_USERNAME")
        self.PASSWORD = getenv("MONGODB_PASSWORD")
        self.PORT = getenv("MONGODB_PORT")
        self.HOST = getenv("MONGODB_HOST")
        self.DATABASE = getenv("MONGODB_DATABASE")

    def client(self):
        """
            ...
        """

        # client=MongoClient(f"mongodb://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}")
        client = MongoClient(
            f"mongodb://{self.HOST}:{self.PORT}/potencia?directConnection=true")
        return client
