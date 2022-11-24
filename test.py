from os import getenv
from sys import path, argv
from time import sleep
from datetime import datetime, timedelta

from Controllers.SaveOnus import SaveONUs
from Database.Connectionmdb import MongoConnection

path.insert(0, ".") # Configure path.

from Controllers.Methods import FTPMethods
# from potencia.Controllers.DeleteDataOnus import DeleteDataOnus
from Connection.ftp import FTPService


# Carregando variáveis de ambiente.
from Config.env import EnvConfig
EnvConfig().load_env()

