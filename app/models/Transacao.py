from config.database_config import conectar_banco
from app.models.Produto import coletar_produto, atualizar_estoque

def compra (idFornecedor: int, idProduto: int, quantidade: int, custoTotal: float, data: str):
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

def venda (idProduto: int, quantidade: int, valorVenda: float, data: str):
    conn = conectar_banco()
    cursor = conn.cursor()

    try: 
        estoque: int = coletar_produto(idProduto, idProduto, "Estoque")
        

        if estoque < quantidade:
            nome: str = coletar_produto(idProduto, idProduto, "NomeProduto")
            raise ValueError (f"Não possue estoque insuficiente de: {nome} ")

        else:
            custo: float = coletar_produto(idProduto, idProduto, "CustoMedio") * quantidade
            lucro: float = valorVenda - custo
            estoqueAtual: int = estoque - quantidade

            atualizar_estoque(idProduto, estoqueAtual)

            cursor.execute(f"""
                insert into tbVendaProduto (idProduto, Quantidade, ValorCusto, ValorVenda, ValorLucro,Data)
			        values ({idProduto}, {quantidade}, {custo}, {valorVenda}, {lucro}, {data})
                """)

    except ValueError as e:
        print(e)
        return None
    
    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

def consulta (tabela: str,coluna: str, filtro):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT FROM {tabela}
                where {coluna} = {filtro}
            """)
        tabela = cursor.fetchall()
        
        if not tabela:
            raise ValueError ("Não foi encontrado vendas com base no filtro passado!")

    except ValueError as e:
        print(e)
        return None

    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()
    
    return tabela

def consulta_venda (colunaDesejada: str,coluna: str, filtro):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT {colunaDesejada}
            FROM tbVendaProduto
                where {coluna} = {filtro}
            """)
        tabela = cursor.fetchall()
        
        if not tabela:
            raise ValueError ("Não foi encontrado vendas com base no filtro passado!")

    except ValueError as e:
        print(e)
        return None

    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()
    
    return tabela

def faturamento (data: str):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        if consulta("tbVendaProduto","Data", data):
            if not consulta("tbFaturamentoVenda", "Data", data):

                valorCusto: float = sum(consulta_venda("ValorCusto","Data", data))
                valorVenda: float = sum(consulta_venda("ValorVenda","Data", data))
                valorLucro: float = sum(consulta_venda("ValorLucro","Data", data))

                cursor.execute(f"""
                    insert into tbFaturamentoVenda (ValorCusto, ValorVenda, ValorLucro, Data)
		                values ({valorCusto}, {valorVenda}, {valorLucro}, {data})
                    """)
                
                conn.commit()
            
            else:
                raise ValueError ("Já foi realizado o faturamento dessa data!")
        else:
            raise ValueError ("Não houve vendas nessa data!")
    
    except ValueError as e:
        conn.rollback()
        print(e)

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()





