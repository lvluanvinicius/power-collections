from os import getenv
from sys import path
from datetime import datetime
from pandas import DataFrame, read_csv
from Controllers.Methods import FTPMethods

from Database.Connection import MysqlConnection

# Configure path.
path.insert(0, "../")

# Carregando variáveis de ambiente.
from Config.env import EnvConfig
EnvConfig().load_env()


class DeleteDataOnus(object):
    
    def __init__(self):
        self.TABLE = "gpon_onus"   

    def delete_data_onus(self, before_date):
        
        # Inciando comunicação com banco de dados.
        with MysqlConnection().connection() as conn:
        
            # Checando status de conexão e salvando dados.
            if conn.is_connected():
                
                # Criando SQL Query.
                sql = f"""
                    DELETE FROM gpon_onus WHERE from_unixtime(COLLECTION_DATE)<%s
                """
                
                # Criando cursor.
                cursor = conn.cursor()
                                
                # Executando query de consulta.
                consult = cursor.execute(sql, (before_date,))
                
                # Transformando dados.
                rows_afected = cursor.rowcount
                                
                # Registrando execução.
                conn.commit()    
                
                return rows_afected #