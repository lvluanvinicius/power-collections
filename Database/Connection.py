from os import getenv
from sys import path
import mysql.connector

# Configure path.
path.insert(0, "../")

# Carregando variáveis de ambiente.
from Config.env import EnvConfig
EnvConfig().load_env()


class MysqlConnection(object):
    
    def __init__(self, *args, **kwargs):
        self.HOST = getenv("MYSQL_HOST")
        self.PORT = getenv("MYSQL_PORT") 
        self.USERNAME = getenv("MYSQL_USERNAME")
        self.PASSWORD = getenv("MYSQL_PASSWORD")
        self.DATABASE = getenv("MYSQL_DATABASE")
    
    def __str__(self):
        return f"Config Mysql: [Host {self.HOST} and port {self.PORT}]"
    
    def connection(self):
        try:
            conn =  mysql.connector.connect(
                host=self.HOST,
                user=self.USERNAME,
                port=self.PORT,
                password=self.PASSWORD,
                database=self.DATABASE,
                auth_plugin='mysql_native_password'
            )    
            return conn
            
        except Exception as err:
            print(err)
            exit()

        
if __name__=="__main__":
    myConn = MysqlConnection()
    myConn.connection()