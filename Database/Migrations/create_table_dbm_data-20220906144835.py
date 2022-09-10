from sys import path
path.insert(0, ".") # Configure path.

from Database.Connection import MysqlConnection

TABLE = "gpon_onus"

with MysqlConnection().connection() as conn: 
    if conn.is_connected():

        # Deleltando se já existir.
        dropSql = f"DROP TABLE IF EXISTS gpon_onus"
        cursor = conn.cursor().execute(dropSql)
        
        # Salvando alterações.
        conn.commit()
        
        # Criando SQL Query.
        sql = f"""                    
                    CREATE TABLE {TABLE} (
                        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        NAME VARCHAR(255) NOT NULL,
                        SERIAL VARCHAR(191) NOT NULL,
                        DEVICE VARCHAR(191) NOT NULL,
                        PON VARCHAR(21) NOT NULL,
                        ONUID int NOT NULL,
                        RX float NOT NULL DEFAULT 0.0,
                        TX float NOT NULL DEFAULT 0.0,
                        COLLECTION_DATE INT NOT NULL
                    )
                """
                
                
        # Criando cursor e executando query.
        cursor = conn.cursor()
        cursor.execute(sql)
        
        # Salvando alterações
        conn.commit()
        
        # Encerrando comunicação.
        cursor.close()
    else:
        print("Erro: banco de dados não conectado!")
