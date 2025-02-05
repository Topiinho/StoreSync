from data.database import conectar_banco

def cadastrar_fornecedor(nome :str, descricao :str):
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            select 1
		    from tbFornecedor
		    where NomeFornecedor = ?
            """, (nome, ))
        tabela = cursor.fetchone()

        if tabela:
            cursor.execute("""
                update tbFornecedor
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

def listar_fornecedor (filtro, coluna :str):
    conn = conectar_banco("database")
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

def coletar_fornecedor (filtro, coluna :str, coluna_desejada :str):
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT ? 
            FROM tbFornecedor
            where ? = ?
            """, (coluna_desejada, coluna, filtro))
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

def verifica_cadastro (nome: str):
    conn = conectar_banco("database")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            select 1
		    from tbFornecedor
		    where NomeFornecedor = ?
            """, (nome, ))
        tabela = cursor.fetchall()

    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()
    
    return tabela[0]
    


class fornecedor:
    def __init__(self, nome: str):
        self.nome = nome

    def cadastrar(self, descricao: str):
        conn = conectar_banco("database")
        cursor = conn.cursor()
        nome = self.nome

        try:
            id = verifica_cadastro(nome)

            if id:
                raise ValueError ("Fornecedor cadastrado")

            cursor.execute("""
                insert into tbFornecedor (NomeFornecedor, dsFornecedor)
	    	        values (?, ?)
                """, (nome, descricao))
            print("Fornecedor cadastrado com sucesso!")
            conn.commit()

        except ValueError as e:
            print(e)
            return None

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()
        
    def atualziar_descricao(self, descricao: str):
        conn = conectar_banco("database")
        cursor = conn.cursor()

        try: 
            nome = self.nome
            id = verifica_cadastro(nome)
            
            if id:
                raise ValueError ("Fornecedor cadastrado")

            cursor.execute("""
                update tbFornecedor
			        set dsFornecedor = ?
			        where NomeFornecedor = ?
                """, (descricao, nome))
            print("Descrição atualizado com sucesso!")
            conn.commit()
            
        except ValueError as e:
            print(e)
            return None

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()






        






