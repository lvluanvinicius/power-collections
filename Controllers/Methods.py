from os import getenv, path as ph, remove, unlink
from sys import path
from datetime import datetime
import time
path.insert(0, "../") # Configure path.


# Carregando variáveis de ambiente.
from Config.env import EnvConfig
EnvConfig().load_env()


class FTPMethods(object):
    
    def __init__(self):
        self.WORKDIR = getenv("WORKDIR")
        self.STORAGEDIR = getenv("STORAGEDIR")
        self.LOCALFILE = ""
    
    def __str__(self):
        print(f"FTP Methods Controller.")
        
    
    def get_files_lists(self, service):
        files = []
        # Configurando diretório de trabalho.
        service.cwd(self.WORKDIR)
        
        # Listando os arquivos existentes.
        service.dir(files.append)
        
        return files;

    # Busca pelo ultimo arquivo de backup armazenado no FTP.
    #
    # service = {type FTPService}
    # return string
    def get_file_name(self, service):        
        files = []
        # Configurando diretório de trabalho.
        service.cwd(self.WORKDIR)
        
        # Listando os arquivos existentes.
        service.dir(files.append)
       
        # Buscando o último arquivo de backup.
        fileName = files[-1].split()[-2] + " " + files[-1].split()[-1]        
        
        return fileName # Retornando nome de arquivo formtado.
    
    
    # Formatação e retorno de data e hora atribuidos no nome de arquivo de backup.
    # 
    # fileName = {type string}
    # @return 2022-01-01 10:00:02
    def get_date_in_file(self, fileName):
        # Gerando data e hora de coleta.
        data = f"{fileName.split('-')[1][:4]}-{fileName.split('-')[1][4:6]}-{fileName.split('-')[1][6:8]} {fileName.split('-')[2].split('_')[0][0:2]}:{fileName.split('-')[2].split('_')[0][2:4]}:{fileName.split('-')[2].split('_')[0][4:6]}"
        
        data2 = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        return (time.mktime(data2.timetuple()))
    
    # Verificação de existência do arquivo de configuração.
    # 
    # @return boolean
    def compare_file(self):
        return ph.isfile(f"{self.STORAGEDIR}/{self.LOCALFILE}")

    
    # Download do arquivo de backup.
    #
    # @return void
    def download_file(self, service):
        # Configurando arquivo de trabalho no FTP.
        service.cwd(self.WORKDIR)
        
        # Ativando modo passivo.
        service.set_pasv(True)
        
        # Carregando nome de arquivo com path de destino.
        file_name=f"{self.STORAGEDIR}/{self.LOCALFILE}"
        
        # Criando e abrindo para escrita o arquivo de backup em storage/data.  
        with open(file_name, "wb") as download:
            # Carregando dados do arquivo, baixando e escrevendo no file em storage/data.
            response = service.retrbinary(f"RETR {self.LOCALFILE}", download.write, 1024)
            
            # Verificando status de execução do download.
            if not response.startswith('226 Transfer complete'):
                
                # Caso não haja sucesso, será removida o arquivo de tentativa em storage/data.
                if ph.isfile(file_name):
                    remove(file_name)
                    
                    
    
    # Exclusão de arquivos.
    #
    # @return void              
    def remove_file(self, service, files):
        # Carregando os arquivos mais antigos.
        files_for_delete = files[:int(getenv("DELETE_FILES_NUMBER"))]
        
        # Configurando diretório de trabalho.
        service.cwd(self.WORKDIR)
        
        # Percorrendos a lista de nomes enviado pelo controlador main.
        for fs in files_for_delete:            
            try:
                # Carregando nome do arquivo.
                self.LOCALFILE = fs.split()[-2]+ " " +fs.split()[-1]
                
                # Realizando a exclusão do aquivo.
                service.delete(self.LOCALFILE)
                
                # Verificando se o arquivo existe para ser excluído no diretório do storage/data.
                if ph.isfile(f"{self.STORAGEDIR}/{self.LOCALFILE}"):
                    
                    # Excluindo no diretório storage/data.
                    unlink(f"{self.STORAGEDIR}/{self.LOCALFILE}")
                    
            except Exception as err:
                print(f"[{datetime.today()}] Error: {err}")
                continue
