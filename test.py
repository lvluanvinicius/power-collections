from os import getenv
from sys import path, argv
from time import sleep
from datetime import datetime, timedelta

from Controllers.SaveOnus import SaveONUs

path.insert(0, ".") # Configure path.

from Controllers.Methods import FTPMethods
# from potencia.Controllers.DeleteDataOnus import DeleteDataOnus
from Connection.ftp import FTPService



# Carregando variáveis de ambiente.
from Config.env import EnvConfig
EnvConfig().load_env()



# Criando Class Methods
methodFtp = FTPMethods()

# Criando conexão
ftp_connection = FTPService().connection()

# Carregando Nome do Arquivo de acordo com o ultimo adicionado.
# methodFtp.LOCALFILE = methodFtp.get_file_name(service=ftp_connection)
# methodFtp.LOCALFILE = "ONU Inventory-20221029-190003_458735964.csv"

svo = SaveONUs()
svo.save_onus_mongo(fileName=methodFtp.LOCALFILE)