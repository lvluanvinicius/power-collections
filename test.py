from os import getenv
from sys import path, argv
from time import sleep
from datetime import datetime

path.insert(0, ".") # Configure path.

from Controllers.Methods import FTPMethods
from Connection.ftp import FTPService


# Carregando variáveis de ambiente.
from Config.env import EnvConfig
EnvConfig().load_env()

# Criando Class Methods
methodFtp = FTPMethods()
                    
# Criando conexão
ftp_connection = FTPService().connection()

files = methodFtp.get_files_lists(service=ftp_connection);
methodFtp.remove_file(service=ftp_connection, files=files);