from os import getenv
from sys import path
# path.insert(0, "../") # Configure path.

from ftplib import FTP

# Carregando variáveis de ambiente.
from Config.env import EnvConfig
EnvConfig().load_env()

class FTPService(object):
    
    def __init__ (self):
        self.HOSTNAME = getenv("FTP_HOST")
        self.USERNAME = getenv("FTP_USERNAME")
        self.PASSWORD = getenv("FTP_PASSWORD")
        
    
    def __str__(self):
        print(f"FTP Service Connection.")
        
    
    def connection(self):
        ftp = FTP()
        ftp.connect(self.HOSTNAME)
        ftp.login(self.USERNAME, self.PASSWORD)
        return ftp
       

