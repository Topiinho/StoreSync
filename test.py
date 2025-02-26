# from datetime import datetime
# from app.models.Produto import listar_produtos
# from app.models.Produto import cadastrar_produto
# from app.models.Fornecedor import listar_fornecedor
# from app.models.Fornecedor import cadastrar_fornecedor
# from app.models.Transacao import compra
# from app.models.Transacao import venda
# from app.models.Transacao import faturamento

# data :str = datetime.now()
# data1 = data.strftime("%d/%m/%Y %H:%M:%S")
# print("Data e hora formatada:", data1)

# data2 = data.strftime("%d/%m/%Y")
# print("Data e hora formatada:", data2)


# cadastrar_produto("Johnny", "Tom", 24, 13, "1", "1")
# cadastrar_produto("Addie", "Jesse", 18, 10, "1", "1")
# cadastrar_produto("Fannie", "Hattie", 18, 37, "1", "1")
# cadastrar_produto("Jacob", "Rosalie", 4, 50, "5", "1")

# cadastrar_fornecedor("Francis Rodriguez", "557817798")
# cadastrar_fornecedor("Herbert Clarke", "4157360950")
# cadastrar_fornecedor("Rosalie Marsh", "3124438918")
# cadastrar_fornecedor("Matilda McDaniel", "1524577529")

# listar_produtos("Todos", "a")
# print("-----------------------------------------------")
# listar_fornecedor("Todos", "a")

# compra(5, 5, 100, 2400, data1)
# compra(6, 6, 100, 1800, data1)
# compra(7, 7, 100, 1800, data1)
# compra(8, 8, 100, 420, data1)

# vendas = [
#     [5, 1, 150],
#     [6, 2, 40],
#     [7, 4, 80],
#     [8, 20, 100]
# ]

# venda(vendas, data1)

# faturamento(data2)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------

from app.controllers.controleProduto import productList

df_retorno = productList()
print(df_retorno)














# CTRL + / para comentar uma linha