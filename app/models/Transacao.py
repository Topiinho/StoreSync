import time
from data.database import conectar_banco
from app.models.Produto import coletar_produto, atualizar_estoque

def compra (idFornecedor: int, idProduto: int, quantidade: int, custoTotal: float, data: str):
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        custoUnitario: float = custoTotal / quantidade

        cursor.execute("""
            insert into tbCompra(idProduto, idFornecedor, CustoUnitario, Quantidade, CustoTotal, Data)
	        	values (?, ?, ?, ?, ?, ?);
            """, (idProduto, idFornecedor, custoUnitario, quantidade, custoTotal, data))
        
        estoque: int = (coletar_produto(conn, cursor, idProduto, "idProduto", "Estoque"))[0]
        custoMedio: float = (coletar_produto(conn, cursor, idProduto, "idProduto", "CustoMedio"))[0]

        custoMedio = (custoTotal + (custoMedio * estoque)) / (estoque + quantidade)
        estoque = estoque + quantidade

        cursor.execute("""
            update tbProduto
		        set Estoque = ?,
			        CustoMedio = ?
		        where idProduto = ?
            """, (estoque, custoMedio, idProduto))
        
        conn.commit()
        print("Compra realziada com sucesso!")
    
    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

def venda_produto (conn, cursor, idVenda: int,idProduto: int, quantidade: int, valorVenda: float, data: str):
    try: 
        estoque: int = coletar_produto(conn, cursor, idProduto, "idProduto", "Estoque")[0]
        

        if estoque < quantidade:
            nome: str = coletar_produto(conn, cursor, idProduto, "idProduto", "NomeProduto")
            raise ValueError (f"Não possue estoque suficiente de: {nome} ")

        else:
            custo: float = coletar_produto(conn, cursor, idProduto, "idProduto", "CustoMedio")[0] * quantidade
            lucro: float = valorVenda - custo
            estoqueAtual: int = estoque - quantidade

            atualizar_estoque(conn, cursor, idProduto, estoqueAtual)

            cursor.execute("""
                insert into tbVendaProduto (idVenda, idProduto, Quantidade, ValorCusto, ValorVenda, ValorLucro, Data)
			        values (?, ?, ?, ?, ?, ?, ?)
                """, (idVenda, idProduto, quantidade, custo, valorVenda, lucro, data))

    except ValueError as e:
        print(e)
        return None
    
    except Exception as e:
        conn.rollback()
        raise e

def venda (vendas: list, data: str):
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        ValorCustoTotal: float = 0
        ValorVendaTotal: float = 0

        for produto in vendas:
            idProduto, quantidade, valorVenda = produto
            print(idProduto, quantidade, valorVenda)

            estoque: int = coletar_produto(conn, cursor, idProduto, "idProduto", "Estoque")[0]
            if estoque < quantidade:
                nome: str = coletar_produto(conn, cursor, idProduto, "idProduto", "NomeProduto")[0]
                raise ValueError (f"Não possue estoque suficiente de: {nome} ")

            custo: float = coletar_produto(conn, cursor, idProduto, "idProduto", "CustoMedio")[0] * quantidade
            print(custo, quantidade, coletar_produto(conn, cursor, idProduto, "idProduto", "CustoMedio")[0])

            ValorCustoTotal += (custo)
            ValorVendaTotal += valorVenda
            print(ValorCustoTotal, ValorVendaTotal)
            print("----------------")

            del estoque, custo
        
        ValorLucroTotal: float = ValorVendaTotal - ValorCustoTotal

        cursor.execute("""
            INSERT INTO tbVenda (ValorCustoTotal, ValorVendaTotal, ValorLucroTotal, Data)
                VALUES (?, ?, ?, ?)
            """, (ValorCustoTotal, ValorVendaTotal, ValorLucroTotal, data))
        
        idVenda = cursor.lastrowid

        for produto in vendas:
            idProduto, quantidade, valorVenda = produto
            venda_produto(conn, cursor, idVenda, idProduto, quantidade, valorVenda, data)

        conn.commit()
        print("Vendas registradas com sucesso!")

    except ValueError as e:
        print(e)
        return None
    
    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()

def consulta_venda (colunaDesejada: str,coluna: str, filtro):
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT {colunaDesejada}
            FROM tbVendaProduto
                where {coluna} = ?
            """, (filtro, ))
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
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM tbVendaProduto 
                WHERE SUBSTR(Data, 1, 10) = ? -- Extrai "DD/MM/YYYY"
            )
        """, (data,))  # data deve ser "DD/MM/YYYY"
        existe_venda = cursor.fetchone()[0]
        print(existe_venda)

        if existe_venda:

            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM tbFaturamentoVenda 
                    WHERE SUBSTR(Data, 1, 10) = ?
                )
            """, (data,))
            existe_faturamento = cursor.fetchone()[0]
            
            if not existe_faturamento:

                cursor.execute("""
                    SELECT 
                        SUM(ValorCusto), 
                        SUM(ValorVenda), 
                        SUM(ValorLucro) 
                    FROM tbVendaProduto 
                    WHERE SUBSTR(Data, 1, 10) = ?
                """, (data,))
                valores = cursor.fetchone()
                
                valorCusto, valorVenda, valorLucro = valores

                cursor.execute("""
                    insert into tbFaturamentoVenda (ValorCusto, ValorVenda, ValorLucro, Data)
		                values (?, ?, ?, ?)
                    """, (valorCusto, valorVenda, valorLucro, data))
                
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





