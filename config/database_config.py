import pyodbc

def conectar_banco():
    try:
        conn = pyodbc.connect(
            'driver={SQL Server};'
            'server=Topiinho\SQLEXPRESS;'
            'database=dbMoonLight;'
            'uid=MoonLightConnect;'
            'pwd=MoonLight'
        )
        print("Conexão com o banco de dados estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
