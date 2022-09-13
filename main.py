from os import getenv
from sys import path, argv
from time import sleep
from datetime import datetime
path.insert(0, ".") # Configure path.

from Controllers.Methods import FTPMethods
from Controllers.SaveOnus import SaveONUs
from Connection.ftp import FTPService

# Carregando variáveis de ambiente.
from Config.env import EnvConfig
EnvConfig().load_env()


# Verificando se foi informado algum argumento.
if len(argv) <= 1:
    print("Informe a ação que quer executar!")
    exit()

# Iniciando processo de coleta.
if argv[1] == "load-onus":
    while True:
        sleep(int(getenv('UPDATE_TIME_LOADS_ONUS')))          
        try: 
            # Criando Class Methods
            methodFtp = FTPMethods()

            # Criando conexão
            ftp_connection = FTPService().connection()

            # Carregando Nome do Arquivo de acordo com o ultimo adicionado.
            methodFtp.LOCALFILE = methodFtp.get_file_name(service=ftp_connection)
            
            # Comparando se o arquivo já existe.
            if not methodFtp.compare_file():
                # Realizando o Download do último arquivo de backup.
                methodFtp.download_file(service=ftp_connection)


                # Encerrando comunicação com FTP.
                ftp_connection.quit()
                
                # Inciando instancia da tabela de onus.
                svo = SaveONUs()
                # Salvando os dados na base de dados.
                svo.save_onus(fileName=methodFtp.LOCALFILE)
                print(f"[{datetime.today()}] Success: Coleta salva com sucesso!")
                
                # Realizando a exclusão dos arquivos antigos.
                try:
                    # Buscando a lista de arquivos.
                    files = methodFtp.get_files_lists(service=ftp_connection);
                    
                    # Realizando a remoção.
                    methodFtp.remove_file(service=ftp_connection, files=files);
                    
                except Exception as err:
                    print(f"[{datetime.today()}] Error: {err}")
                                
            else:            
                print(f"[{datetime.today()}] Success: Nenhuma coleta encontrada!")            
            
        except Exception as err:
            print(f"[{datetime.today()}] Error: {err}")
            continue
        

else: 
    print("Informe uma ação válida!")
