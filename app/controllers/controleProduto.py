from app.models.Produto import Product_Service, Produto
import pandas as pd
import tempfile
from PIL import Image
import io
import os
import threading



class Product_Control:

    def blob_to_temp_file(blob):
        try:
            # Converte o blob em um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                temp_file_path = temp_file.name  # Guarda o caminho antes de fechar o arquivo
            
            # Abre a imagem, salva e fecha
            image = Image.open(io.BytesIO(blob))
            image.save(temp_file_path, format='PNG')
            image.close()  # Fecha a imagem para liberar o arquivo

            # Aguarda 10 segundos antes de excluir (pode aumentar o tempo se necessário)
            threading.Timer(10, lambda: os.remove(temp_file_path) if os.path.exists(temp_file_path) else None).start()

            return temp_file_path
        except Exception as e:
            print(f"Erro ao criar arquivo temporário: {e}")
            return None


    def product_List(filtro: str):
        try:
            # Verifica se o filtro é "Todos"
            if filtro.lower() == "todos" or filtro == None or filtro == "":    
                ids = Product_Service.listar_produtos_id()
                produtos_lista = []

                for id in ids:
                    produto = Produto(id)
                    produtos_lista.append({
                        "id": produto.Id,
                        "nome": produto.Nome,
                        "modelo": produto.Modelo,
                        "custo": produto.CustoMedio,
                        "estoque": produto.Estoque,
                        "blob": produto.Foto
                    })

                if produtos_lista:
                    df = pd.DataFrame(produtos_lista)
                    df["foto"] = df["blob"].apply(lambda blob: Product_Control.blob_to_temp_file(blob))
                    df_filtrado = df[["id", "nome", "modelo", "custo", "estoque", "foto"]].sort_values(by="nome")
                    return df_filtrado.to_records(index=False).tolist()
                else:
                    return []

                
            # Verifica se o filtro é um nome de produto
            else:
                ids = Product_Service.listar_produtos_id()
                produtos_lista = []
                for id in ids:
                    produto = Produto(id)
                    produto_nome_clean = produto.Nome.strip().lower()
                    # Verifica se o filtro está contido no nome do produto
                    if filtro.lower() in produto_nome_clean:
                        produtos_lista.append({
                            "id": produto.Id,
                            "nome": produto.Nome,
                            "modelo": produto.Modelo,
                            "custo": produto.CustoMedio,
                            "estoque": produto.Estoque,
                            "blob": produto.Foto
                        })
                if produtos_lista:
                    df = pd.DataFrame(produtos_lista)
                    df["foto"] = df["blob"].apply(lambda blob: Product_Control.blob_to_temp_file(blob))
                    df_filtrado = df[["id", "nome", "modelo", "custo", "estoque", "foto"]].sort_values(by="nome")
                    return df_filtrado.to_records(index=False).tolist()
                else:
                    return []

        except Exception as e:
            raise e


    def novo_Cadastro(nome: str, modelo: str, custo: float, estoque: int, foto: str):
        try:
            with open(foto, "rb") as file:
                blob = file.read()

            Product_Service.cadastrar_produto(nome, modelo, custo, estoque, blob)
        except Exception as e:
            raise e


    def atualiza_Cadastro(id: int, nome: str, modelo: str, custo: float, estoque: int, foto: str):
        try:
            produto = Produto(id)

            if os.path.exists(foto):
                with open(foto, "rb") as file:
                    blob = file.read()   
                
                    produto.atualizar_nome(nome)
                    produto.atualizar_modelo(modelo)
                    produto.atualizar_custoMedio(custo)
                    produto.atualizar_estoque(estoque)
                    produto.atualizar_foto(blob)
            
            else:
                    produto.atualizar_nome(nome)
                    produto.atualizar_modelo(modelo)
                    produto.atualizar_custoMedio(custo)
                    produto.atualizar_estoque(estoque)

        except Exception as e:
            raise e


