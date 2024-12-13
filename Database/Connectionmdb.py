from pymongo import MongoClient
from Config.env import EnvConfig
from os import getenv
from sys import path
import logging


# Configuração básica do logger
logging.basicConfig(
    filename='/app/logs/main.log',  # Caminho do arquivo de log
    level=logging.DEBUG,              # Nível do log
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato da mensagem
)


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

        logging.error(f"Erro ao parsear linha: {self.HOST}:{self.PORT}")

    def client(self):
        """
            ...
        """
        # Criando conexão direta com o mongo db. 
        # client=MongoClient(port=int(self.PORT), host=self.HOST, password=self.PASSWORD, username=self.USERNAME, authSource='admin')
        client = MongoClient(f"mongodb://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?authSource=admin&authMechanism=SCRAM-SHA-256")
            


        
        return client
