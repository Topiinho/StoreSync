from app.models.Produto import listar_produtos, cadastrar_produto
import pandas as pd
import tempfile
from PIL import Image
import io
import os
import threading

def blob_to_temp_file(blob, temp_files):
    try:
        # Converte o blob em um arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            # Cria uma imagem a partir do blob
            image = Image.open(io.BytesIO(blob))

            # Salva a imagem no arquivo temporário
            image.save(temp_file, format='PNG')

            print(f"Arquivo temporário salvo em: {temp_file.name}")

            # Adiciona o caminho do arquivo à lista de arquivos temporários
            temp_files.append(temp_file.name)
            
            return temp_file.name
    except Exception as e:
        raise e

def productList(filtro):
    try:
        if filtro == "Todos":
            tabela = listar_produtos("Todos", "")
            df = pd.DataFrame(tabela, columns=["id", "nome", "modelo", "custo", "estoque", "blob"])
            df["modelo"] = df["modelo"].fillna("Único")

            # Lista para armazenar os caminhos dos arquivos temporários
            temp_files = []

            # Converte o blob em arquivos temporários e armazena o caminho
            df["foto"] = df["blob"].apply(lambda blob: blob_to_temp_file(blob, temp_files))

            df_filtrado = df[["nome", "modelo", "custo", "estoque", "foto"]].sort_values(by="nome")

            limpar_temp_arquivos(temp_files)

            return df_filtrado.to_records(index=False).tolist()
        
        elif filtro == "" or filtro == None:
            return productList("Todos")
        
        else:
            tabela = listar_produtos(filtro, "NomeProduto")
            df = pd.DataFrame(tabela, columns=["id", "nome", "modelo", "custo", "estoque", "blob"])
            df["modelo"] = df["modelo"].fillna("Único")

            # Lista para armazenar os caminhos dos arquivos temporários
            temp_files = []

            # Converte o blob em arquivos temporários e armazena o caminho
            df["foto"] = df["blob"].apply(lambda blob: blob_to_temp_file(blob, temp_files))

            df_filtrado = df[["nome", "modelo", "custo", "estoque", "foto"]].sort_values(by="nome")

            limpar_temp_arquivos(temp_files)

            return df_filtrado.to_records(index=False).tolist()

    except Exception as e:
        raise e

def delete_temp_file(file_path):
    try:
        os.remove(file_path)
        print(f"Arquivo temporário removido: {file_path}")
    except Exception as e:
        raise e

def limpar_temp_arquivos(temp_files):
    # Espera 5 segundos (ou o tempo que você achar necessário)
    threading.Timer(5, lambda: [delete_temp_file(f) for f in temp_files]).start()

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
   
