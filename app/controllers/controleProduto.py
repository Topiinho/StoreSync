import pandas as pd
from app.models.Produto import listar_produtos, cadastrar_produto

def productList():
    tabela = listar_produtos("Todos", "")

    # Criando um DataFrame com os nomes das colunas corretos
    df = pd.DataFrame(tabela, columns=["id", "nome", "modelo", "tags", "custo", "estoque", "descricao"])
    
    # Substituir valores nulos
    df["modelo"] = df["modelo"].fillna("Único")
    df["descricao"] = df["descricao"].fillna("Sem descrição")

    # Filtrando apenas as colunas desejadas
    df_filtrado = df[["nome", "modelo", "custo", "estoque", "descricao"]]

    # Ordenando alfabeticamente pelo nome
    df_filtrado = df_filtrado.sort_values(by="nome")

    # Convertendo para lista de tuplas
    return df_filtrado.to_records(index=False).tolist()

def novoCadastro(nome: str, modelo: str, custo: float, estoque: int, tags: str, descricao: str):
    try:
        cadastrar_produto(nome, modelo, custo, estoque, tags, descricao)
    except Exception as e:
        raise e
   
