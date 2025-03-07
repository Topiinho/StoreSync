import pandas as pd
import base64
from app.models.Produto import listar_produtos, cadastrar_produto

def blob_Imagem(blob):
    try:
        print("Convertendo blob para base64")
        foto = base64.b64encode(blob).decode("utf-8")
        print("Base64 gerado com sucesso")
        return foto
    except Exception as e:
        print(f"Erro na conversão do BLOB para base64: {e}")
        raise e


def productList():
    try:
        tabela = listar_produtos("Todos", "")
        print(tabela)  # Verifique se a coluna blob contém dados válidos
        df = pd.DataFrame(tabela, columns=["id", "nome", "modelo", "custo", "estoque", "blob"])
        print(df)
        df["modelo"] = df["modelo"].fillna("Único")
        df["foto"] = df["blob"].apply(blob_Imagem)

        df_filtrado = df[["nome", "modelo", "custo", "estoque", "foto"]]
        df_filtrado = df_filtrado.sort_values(by="nome")
        print(df_filtrado)

        return df_filtrado.to_records(index=False).tolist()

    except Exception as e:
        raise e


def imagem_Blob(foto: str):
    try:
        with open(foto, "rb") as file:
            blob = file.read()
        return blob
    except Exception as e:
        raise e

def novoCadastro(nome: str, modelo: str, custo: float, estoque: int, foto: str):
    try:
        blob = imagem_Blob(foto)
        cadastrar_produto(nome, modelo, custo, estoque, blob)
    except Exception as e:
        raise e
   
