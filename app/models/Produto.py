from config.database_config import conectar_banco

def cadastrar_produto (nome, modelo, custoMedio, estoque, tags, descricao):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            select 1
	    	from tbProduto
	    	where NomeProduto = ?
	    		and Modelo = ?
            """,(nome, modelo))
        retorno = cursor.fetchone()

        if retorno :
            cursor.execute("""
            update tbProduto
	    		set Descricao = ?,
                    Tags = ?
	    		where NomeProduto = ?
	    			and Modelo = ?
            """, (descricao, tags, nome, modelo))
        else:
            cursor.execute(f"""
                insert into tbProduto (NomeProduto, Modelo, Tags, CustoMedio, Estoque, Descricao)
	    	        values (?,?,?,?,?,?)
            """,(nome, modelo, tags, custoMedio, estoque, descricao))
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    
    finally:
        cursor.close()
        conn.close()

def listar_produtos (filtro, coluna):
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