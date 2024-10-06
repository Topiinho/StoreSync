from config.database_config import conectar_banco
from app.models.Produto import coletar_produto

def compra (idFornecedor: int, idProduto: int, quantidade: int, custoTotal: int, data: str):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        custoUnitario = custoTotal / quantidade

        cursor.execute(f"""
            insert into tbCompra(idProduto, idFornecedor, CustoUnitario, Quantidade, CustoTotal, Data)
	        	values ({idProduto}, {idFornecedor}, {custoUnitario}, {quantidade}, {custoTotal}, {data});
            """)
        
        estoque = (coletar_produto(idProduto, "idProduto", "Estoque"))[0]
        custoMedio = (coletar_produto(idProduto, "idProduto", "CustoMedio"))[0]

        custoMedio = (custoTotal + (custoMedio * estoque)) / (estoque + quantidade)
        estoque = estoque + quantidade

        cursor.execute(f"""
            update tbProduto
		        set Estoque = {estoque},
			        CustoMedio = {custoMedio}
		        where idProduto = {idProduto}
            """)
        
        conn.commit()
        print("Compra realziada com sucesso!")
    
    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()