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
            """, (nome, modelo))
        retorno = cursor.fetchone()

        if retorno :
            cursor.execute("""
            update tbProduto
	    		set Descricao = ?
	    		where NomeProduto = ?
	    			and Modelo = ?
            """, (descricao, nome, modelo))
        else:
            cursor.execute("""
                insert into tbProduto (NomeProduto, Modelo, Tags, CustoMedio, Estoque, Descricao)
	    	        values (?, ?, ?, ?, ?, ?)
            """, (nome, modelo, tags, custoMedio, estoque, descricao))
        
        conn.commit()

    except Exception as e:
        # Em caso de erro, desfazemos a transação
        conn.rollback()
        raise e
    
    finally:
        # Fechar cursor e conexão
        cursor.close()
        conn.close()