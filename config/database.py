import sqlite3

def conectar_banco():
    try:
        conn = sqlite3.connect("database.db")
        print("Conexão com o banco de dados estabelecida com sucesso!")



        conn.commit()
        return conn

    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
conectar_banco()