from Config.env import EnvConfig
from Connection.ftp import FTPService
from Controllers.SaveOnus import SaveONUs
from Controllers.Methods import FTPMethods
from Controllers.DeleteDataOnus import DeleteDataOnus
from os import getenv
from sys import path, argv
from time import sleep
from datetime import datetime
path.insert(0, ".")  # Configure path.


# Carregando variáveis de ambiente.
EnvConfig().load_env()


# Verificando se foi informado algum argumento.
if len(argv) <= 1:
    print("Informe a ação a ser executar.")
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
            methodFtp.LOCALFILE = methodFtp.get_file_name(
                service=ftp_connection)

            # Comparando se o arquivo já existe.
            if not methodFtp.compare_file():
                # Realizando o Download do último arquivo de backup.
                methodFtp.download_file(service=ftp_connection)

                # Encerrando comunicação com FTP.
                ftp_connection.quit()

                # Inciando instancia da tabela de onus.
                svo = SaveONUs()

                # Salvando os dados na base de dados.
                # svo.save_onus_mysql(fileName=methodFtp.LOCALFILE)
                svo.save_onus_mongo(fileName=methodFtp.LOCALFILE)
                print(f"[{datetime.today()}] Success: Coleta salva com sucesso.")

            else:
                print(f"[{datetime.today()}] Success: Nenhuma coleta encontrada.")

            # Realizando a exclusão dos arquivos antigos.
            try:
                # Buscando a lista de arquivos.
                files = methodFtp.get_files_lists(service=ftp_connection)

                # Realizando a remoção.
                methodFtp.remove_file(service=ftp_connection, files=files)

                print(
                    f"[{datetime.today()}] Success: Exclusão realizada com sucesso.")

            except Exception as err:
                print(f"[{datetime.today()}] Error: {err}")
                continue

        except Exception as err:
            print(f"[{datetime.today()}] Error: {err}")
            continue


# if argv[1] == "delete-history":
#    dt_time = datetime.strptime(FTPMethods().get_before_date(), '%Y-%m-%d %H:%M:%S')
#    afected = DeleteDataOnus().delete_data_onus(FTPMethods().get_before_date())

else:
    print("Informe uma ação válida.")
    exit()
