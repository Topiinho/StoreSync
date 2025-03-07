from data.database import conectar_banco

def cadastrar_produto (nome :str, modelo :str, custoMedio :float, estoque :int, foto :str):
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
	    	    	set Foto = ?
	    	    	where NomeProduto = ?
	    	    		and Modelo = ?
                """, (foto))
            print("Foto do produto atualizado com sucesso!")

        else:
            cursor.execute("""
                insert into tbProduto (NomeProduto, Modelo, CustoMedio, Estoque, Foto)
	    	        values (?,?,?,?,?)
                """, (nome, modelo, custoMedio, estoque, foto))
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

            return tabela

        else:
            cursor.execute(f"""
                SELECT * 
                FROM tbProduto
                where {coluna} = ?
                """, (filtro, ))
            tabela = cursor.fetchall()
            print("Tabela filtrada:", tabela)  # Verifique o conteúdo da tabela filtrada
            return tabela

    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()

def coletar_produto (cursor, filtro :int, coluna: str, coluna_desejada: str):
    try:
        cursor.execute(f"""
            SELECT {coluna_desejada}
            FROM tbProduto
            where {coluna} = ?
            """, (filtro, ))
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
  
    return i

def atualizar_estoque (conn, cursor, idProduto: int, estoque: int):
    try:
        cursor.execute("""
            update  tbProduto
			set Estoque = ?
			where idProduto = ?
            """, (estoque, idProduto))

        print("Estoque atualizado")

    except Exception as e:
        conn.rollback()
        raise e




