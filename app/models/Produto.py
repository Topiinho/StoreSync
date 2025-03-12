import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from data.database import conectar_banco


class Product_Service:
    
    def cadastrar_produto (nome :str, modelo :str, custoMedio :float, estoque :int, foto :str): # Função para cadastrar um novo produto ou atualizar um produto já cadastrado
        conn = conectar_banco("database")
        cursor = conn.cursor()

        try:
            # Verifica se o produto já está cadastrado
            cursor.execute("""
                select 1
                from tbProduto
                where NomeProduto = ?
                    and Modelo = ?
                """, (nome, modelo))
            tabela = cursor.fetchone()

            if tabela : # Se o produto já estiver cadastrado: Atualiza os dados
                cursor.execute("""
                    update tbProduto
                        set Foto = ?,
                            custoMedio = ?,
                            Estoque = ?
                        where NomeProduto = ?
                            and Modelo = ?
                    """, (foto, custoMedio, estoque, nome, modelo))
                print("Produto atualizado com sucesso!")

            else: # Se o produto não estiver cadastrado: Cadastra o produto
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


    def listar_produtos_id(): # Função para listar os ids dos produtos cadastrados
        conn = conectar_banco("database")
        cursor = conn.cursor()

        try: # Coletar os ids dos produtos cadastrados
            cursor.execute("""
                select idProduto
                from tbProduto;
                """)
            tabela = cursor.fetchall()

            ids = [i[0] for i in tabela] # Transforma a tabela em uma lista de ids

            return ids 
        
        except Exception as e:
            raise e

        finally:
            cursor.close()
            conn.close()

        

class Produto: # Classe para manipular os produtos
    def __init__(self, Id): # Construtor da classe
        self.Id: int = Id
        self.Nome: str = None
        self.Modelo: str = None
        self.CustoMedio: float = None
        self.Estoque: int = None
        self.Foto = None

        self.coletar_produto()


    def coletar_produto (self): # Função para coletar os dados do produto com base no id
        try:
            conn = conectar_banco("database")
            cursor = conn.cursor()

            cursor.execute("""
                SELECT NomeProduto, Modelo, CustoMedio, Estoque, Foto
                FROM tbProduto
                where idProduto = ?
                """, (self.Id, ))
            produto = cursor.fetchall()

            if produto:
                self.Nome = produto[0][0]
                self.Modelo = produto[0][1]
                self.CustoMedio = produto[0][2]
                self.Estoque = produto[0][3]
                self.Foto = produto[0][4]
            else:
                raise ValueError ("Produto não cadastrado")
            
        except ValueError as e:
            raise e

        except Exception as e:
            raise e
        
        finally:
            cursor.close()
            conn.close()
    

    def atualizar_nome (self, new_nome :str): # Função para atualizar o nome do produto
        try:
            conn = conectar_banco("database")
            cursor = conn.cursor()

            cursor.execute("""
                update tbProduto
                set NomeProduto = ?
                where idProduto = ?
                """, (new_nome, self.Id))
            print("Nome atualizado com sucesso!")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()
    

    def atualizar_modelo (self, new_modelo :str): # Função para atualizar o modelo do produto
        try:
            conn = conectar_banco("database")
            cursor = conn.cursor()

            cursor.execute("""
                update tbProduto
                set Modelo = ?
                where idProduto = ?
                """, (new_modelo, self.Id))
            print("Modelo atualizado com sucesso!")

            conn.commit()
        
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()
    

    def atualizar_custoMedio (self, new_custoMedio :float): # Função para atualizar o custo médio do produto
        try:
            conn = conectar_banco("database")
            cursor = conn.cursor()

            cursor.execute("""
                update tbProduto
                set CustoMedio = ?
                where idProduto = ?
                """, (new_custoMedio, self.Id))
            print("Custo médio atualizado com sucesso!")

            conn.commit()
        
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()


    def atualizar_estoque (self, new_estoque :int): # Função para atualizar o estoque do produto
        try:
            conn = conectar_banco("database")
            cursor = conn.cursor()

            cursor.execute("""
                update tbProduto
                set Estoque = ?
                where idProduto = ?
                """, (new_estoque, self.Id))
            print("Estoque atualizado com sucesso!")

            conn.commit()
        
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()
    

    def atualizar_foto (self, new_foto :str): # Função para atualizar a foto do produto
        try:
            conn = conectar_banco("database")
            cursor = conn.cursor()

            cursor.execute("""
                update tbProduto
                set Foto = ?
                where idProduto = ?
                """, (new_foto, self.Id))
            print("Foto atualizada com sucesso!")

            conn.commit()
        
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()
    

    def deletar_produto (self):   # Função para marcar um produto como deletado
        #ajustar o banco de dados para ser possivel marcar um produto como deletado sem realmente apagalo afim de manter o historico
        try:
            conn = conectar_banco("database")
            cursor = conn.cursor()

            ...
        
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()
