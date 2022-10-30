from os import getenv
from sys import path
from pandas import DataFrame, read_csv
from Controllers.Methods import FTPMethods

from Database.Connection import MysqlConnection
from Database.Connectionmdb import MongoConnection

# Configure path.
path.insert(0, "../")

# Carregando variáveis de ambiente.
from Config.env import EnvConfig
EnvConfig().load_env()


class SaveONUs(object):
    
    def __init__(self):
        self.TABLE = "gpon_onus"   
        self.STORAGEDIR=getenv("STORAGEDIR")
        
           
    # Realiza a leitura dos dados contidos no arquivo CSV em storage/data
    # 
    # fileName = {type string}
    # @return DataFrame
    def get_onus_in_csv(self, fileName):
    
        # Carregando os dados do arquivo CSV.
        dfDatacom = DataFrame(
            
            # Carregando arquivo.
            read_csv(f"{self.STORAGEDIR}/{fileName}", low_memory=False),
            
            # Carregando apenas colunas selecionadas de acordo com a lista.
            columns=[
                "Device ID", "Port", "Serial Number", "Name", "Rx Power (dBm)", "Tx Power (dBm)", "ID"
            ]).rename(
                
                # Renomeando as colunas selecionadas.
                columns={
                "Device ID": "DEVICE", "Port": "PORT", "Serial Number":"SERIAL",
                "Name": "NAME", "Rx Power (dBm)": "RXDBM", "Tx Power (dBm)": "TXDBM"
            })
        
        # Retornando DataFrame.
        return dfDatacom
    
    
    
    # Realiza insert na base de dados.
    # 
    # data = {type dict}
    # dataCollection = {type string}
    # conn = {type MysqlConnection}
    # @return void
    def save_mysql(self, data, dataCollection, conn):
        
        # Checando status de conexão e salvando dados.
        if conn.is_connected():
            
            # Criando SQL Query.
            sql = f"""
                INSERT INTO {self.TABLE} (
                    NAME, SERIAL, DEVICE, PON, ONUID, RX, TX, COLLECTION_DATE
                ) VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s
                )
            """
            
            # Salvando e executando query.
            conn.cursor().execute(sql,(
                data["NAME"], data["SERIAL"], 
                data["DEVICE"], data["PORT"], 
                data["ONUID"], data["RXDBM"], 
                data["TXDBM"], int(dataCollection)
            ))
            
            # Registrando execução.
            conn.commit()            
            
    
    # Salva os dados de ONUs do CSV na base de dados.
    #
    # fileName = {type string}
    # @return void
    def save_onus_mysql(self, fileName):
        # Carregando data e hora de coleta.
        dataCollection = FTPMethods().get_date_in_file(fileName=fileName)
        
        # Carregando DataFrame
        dfDatacom = self.get_onus_in_csv(fileName)
        
        # Inciando comunicação com banco de dados.
        with MysqlConnection().connection() as conn:
            
            # Percorrendo dataframe
            for dataVar in dfDatacom.itertuples():            
                if "nan" in str(dataVar.RXDBM) or "nan" in str(dataVar.TXDBM):   
                    data = {
                        "NAME" : dataVar.NAME, 
                        "SERIAL": dataVar.SERIAL, 
                        "DEVICE": dataVar.DEVICE,
                        "PORT": dataVar.PORT, 
                        "ONUID": dataVar.ID, 
                        "RXDBM": float(0.0), 
                        "TXDBM": float(0.0)                        
                    } 
                
                else:
                    data = {
                        "NAME" : dataVar.NAME, 
                        "SERIAL": dataVar.SERIAL, 
                        "DEVICE": dataVar.DEVICE,
                        "PORT": dataVar.PORT, 
                        "ONUID": dataVar.ID, 
                        "RXDBM": dataVar.RXDBM, 
                        "TXDBM": dataVar.TXDBM
                    }
                
                if "nan" in str(data["NAME"]):
                    data["NAME"]=f"NOME_DESCONHECIDO_{dataVar.SERIAL}"
        
                # Enviando dados para serem salvos na base de dados.
                try:
                    self.save_mysql(data=data, dataCollection=dataCollection, conn=conn)
                except Exception as err:
                    print(f"Error: {err}")
                    continue
    
            conn.close()

        

    def save_mongo(self, data, conn):
        insert = conn.potencia.gpon_onus_dbm.insert_many(data)
        
        
    def save_onus_mongo(self, fileName):
        # Carregando data e hora de coleta.
        dataCollection = FTPMethods().get_date_in_file(fileName=fileName)
        
        # Carregando DataFrame
        dfDatacom = self.get_onus_in_csv(fileName)

        
        # Iniciando instancia para dados. 
        # Utilizado para enviar objeto em massa para salvar no MongoDB.
        dataSave=[]

        # Inciando comunicação com banco de dados.
        with MongoConnection().client() as conn:
            # Percorrendo dataframe
            for dataVar in dfDatacom.itertuples():
                if "nan" in str(dataVar.RXDBM) or "nan" in str(dataVar.TXDBM):   
                    data = {
                        "NAME" : dataVar.NAME, 
                        "SERIAL": dataVar.SERIAL, 
                        "DEVICE": dataVar.DEVICE,
                        "PORT": dataVar.PORT, 
                        "ONUID": dataVar.ID, 
                        "RXDBM": float(0.0), 
                        "TXDBM": float(0.0),
                        "COLLECTION_DATE": int(dataCollection)
                    } 
                
                else:
                    data = {
                        "NAME" : dataVar.NAME, 
                        "SERIAL": dataVar.SERIAL, 
                        "DEVICE": dataVar.DEVICE,
                        "PORT": dataVar.PORT, 
                        "ONUID": dataVar.ID, 
                        "RXDBM": dataVar.RXDBM, 
                        "TXDBM": dataVar.TXDBM,
                        "COLLECTION_DATE": int(dataCollection)
                    }
                
                if "nan" in str(data["NAME"]):
                    data["NAME"]=f"NOME_DESCONHECIDO_{dataVar.SERIAL}"
                
                dataSave.append(data)
            
                
            # Enviando dados para serem salvos na base de dados.
            try:
                self.save_mongo(data=dataSave, conn=conn)
            except Exception as err:
                print(f"Error: {err}")

            conn.close()


# Estamos tão desligados da nossa vida, que nem notamos o que estamos fazendo e as vezes esquecemos do que é importante.
