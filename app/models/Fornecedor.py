from config.database_config import conectar_banco

def cadastrar_fornecedor(nome, descricao):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            select 1
		    from tbFornecedor
		    where NomeFornecedor = ?
            """, (nome))
        tabela = cursor.fetchone()

        if tabela:
            cursor.execute("""
                updateupdate tbFornecedor
			        set dsFornecedor = ?
			        where NomeFornecedor = ?
                """, (descricao, nome))
            print("descrição do fornecedor atualizado!")
        
        else:
            cursor.execute("""
                insert into tbFornecedor (NomeFornecedor, dsFornecedor)
		            values (?, ?)
                """, (nome, descricao))
            print("Fornecedor cadastrado com sucesso!")
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

def listar_fornecedor (filtro, coluna):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        if (filtro == "Todos"):
            cursor.execute("""
                select * from tbFornecedor;
                """)
            tabela = cursor.fetchall()

            for row in tabela:
                print(row)

        else:
            cursor.execute("""
                SELECT * 
                FROM tbFornecedor
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

def coletar_fornecedor (filtro, coluna, coluna_desejada):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT {coluna_desejada} 
            FROM tbFornecedor
            where {coluna} = {filtro}
            """)
        tabela = cursor.fetchone()
        
        if tabela:
            i = tabela[0]
        else:
            raise ValueError ("Fornecedor não cadastrado")
    
    except ValueError as e:
        print(e)
        return None

    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()
    
    return i


