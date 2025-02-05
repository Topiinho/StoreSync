from data.database import conectar_banco

def cadastrar_produto (nome :str, modelo :str, custoMedio :float, estoque :int, tags :str, descricao :str):
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            select 1
	    	from tbProduto
	    	where NomeProduto = ?
	    		and Modelo = ?
            """, (nome, modelo))
        tabela = cursor.fetchone()

        if tabela :
            cursor.execute("""
                update tbProduto
	    	    	set Descricao = ?,
                        Tags = ?
	    	    	where NomeProduto = ?
	    	    		and Modelo = ?
                """, (descricao, tags, nome, modelo))
            print("Descrição do produto atualizado com sucesso!")

        else:
            cursor.execute("""
                insert into tbProduto (NomeProduto, Modelo, Tags, CustoMedio, Estoque, Descricao)
	    	        values (?,?,?,?,?,?)
                """, (nome, modelo,tags, custoMedio, estoque, descricao))
            print("Produto cadastro com sucesso!")
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    
    finally:
        cursor.close()
        conn.close()

def listar_produtos (filtro, coluna :str):
    conn = conectar_banco("database")
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
            cursor.execute("""
                SELECT * 
                FROM tbProduto
                where ? = ?
                """, (coluna, filtro))
            tabela = cursor.fetchall()
            
            for row in tabela:
                print(row)

    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()

def coletar_produto (filtro :int, coluna: str, coluna_desejada: str):
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT ?
            FROM tbProduto
            where ? = ?
            """, (coluna_desejada, coluna, filtro))
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
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            update  tbProduto
			set Estoque = ?
			where idProduto = ?
            """, (estoque, idProduto))
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()




