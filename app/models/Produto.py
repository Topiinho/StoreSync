from config.database_config import conectar_banco

def cadastrar_produto (nome :str, modelo :str, custoMedio :float, estoque :int, tags :str, descricao :str):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            select 1
	    	from tbProduto
	    	where NomeProduto = {nome}
	    		and Modelo = {modelo}
            """)
        tabela = cursor.fetchone()

        if tabela :
            cursor.execute(f"""
                update tbProduto
	    	    	set Descricao = {descricao},
                        Tags = {tags}
	    	    	where NomeProduto = {nome}
	    	    		and Modelo = {modelo}
                """)
            print("Descrição do produto atualizado com sucesso!")

        else:
            cursor.execute(f"""
                insert into tbProduto (NomeProduto, Modelo, Tags, CustoMedio, Estoque, Descricao)
	    	        values ({nome},{modelo},{tags},{custoMedio},{estoque},{descricao})
                """)
            print("Produto cadastro com sucesso!")
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    
    finally:
        cursor.close()
        conn.close()

def listar_produtos (filtro, coluna :str):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        if (filtro == "Todos"):
            cursor.execute("""
                select * from tbProduto;
                """)
            tabela = cursor.fetchall()

            for row in tabela:
                print(row)

        else:
            cursor.execute(f"""
                SELECT * 
                FROM tbProduto
                where {coluna} = {filtro}
                """)
            tabela = cursor.fetchall()
            
            for row in tabela:
                print(row)

    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()

def coletar_produto (filtro :int, coluna: str, coluna_desejada: str):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT {coluna_desejada}
            FROM tbProduto
            where {coluna} = {filtro}
            """)
        tabela = cursor.fetchall()
        
        if tabela:
            i = tabela[0]
        else:
            raise ValueError ("Produto não cadastrado")
    
    except ValueError as e:
        print(e)
        return None

    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()
    
    return i

def atualizar_estoque (idProduto: int, estoque: int):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            update  tbProduto
			set Estoque = {estoque}
			where idProduto = {idProduto}
            """)
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()




