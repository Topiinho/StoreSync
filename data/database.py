import sqlite3
import os

def conectar_banco(nome_loja: str):
    try:
        db = f"data/{nome_loja}.db"

        if os.path.isfile(db):
            conn = sqlite3.connect(db)
            print("Conexão com o banco de dados estabelecida com sucesso!")
            return conn
        
        else:
            raise ValueError (f"O banco de dados {nome_loja} não existente!")
        
    except ValueError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        if conn:
            conn.close()
        return None
    
def criar_banco(nome_loja: str):
    try: 
        db = f"data/{nome_loja}.db"
        
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

    except ValueError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        if conn:
            conn.close()
        return None

# conectar_banco("database")