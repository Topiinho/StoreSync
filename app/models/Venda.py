from data.database import Data_Base

def lucro(custo: float, venda: float):
    lucro = venda - custo
    return lucro

class Venda_Service:

    def list_Venda_Ids ():
        try: # Coletar os ids dos produtos cadastrados
            banco = Data_Base("database")
            conn = banco.conectar_Banco()
            cursor = conn.cursor()

            cursor.execute("""
                select idVenda
                from tbVenda;
                """)
            tabela = cursor.fetchall()

            ids = [i[0] for i in tabela] # Transforma a tabela em uma lista de ids

            return ids 
        
        except Exception as e:
            raise e

        finally:
            cursor.close()
            conn.close()


    def list_Product_Venda_Ids():
        try: # Coletar os ids dos produtos cadastrados
            banco = Data_Base("database")
            conn = banco.conectar_Banco()
            cursor = conn.cursor()

            cursor.execute("""
                select idVendaProduto
                from tbVendaProduto;
                """)
            tabela = cursor.fetchall()

            ids = [i[0] for i in tabela] # Transforma a tabela em uma lista de ids

            return ids 
        
        except Exception as e:
            raise e

        finally:
            cursor.close()
            conn.close()


    def _cadastrar_venda(conn, cursor, custo: float, venda: float, data):
        try:
            cursor.execute("""
                insert into tbVenda (Custo, Venda, Data)
                    values (?,?,?)
                """, (custo, venda, data))
            print("Venda cadastrada com sucesso!")
            
            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()


    def _cadastrar_produto_venda(conn, cursor, id_venda: int, id_produto: int, quantidade: int, custo: float, venda: float, data):
        try:
            cursor.execute("""
                insert into tbVendaProduto (idVenda, idProduto, Quantidade, Custo, Venda, Data)
                    values (?,?,?,?,?,?)
                """, (id_venda, id_produto, quantidade, custo, venda, data))
            print("Produto vendido com sucesso!")
            
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()


    def venda(produtos: tuple, custo_total: float, venda_total: float, data):
        try:
            banco = Data_Base("database")
            conn = banco.conectar_Banco()
            cursor = conn.cursor()

            id_venda = Venda_Service._cadastrar_venda(conn, cursor, custo_total, venda_total, data)

            custo_total_confirmado = 0
            venda_total_confirmada = 0

            for produto in produtos:
                id_produto, quantidade, custo, venda = produto
                Venda_Service._cadastrar_produto_venda(conn, cursor, id_venda, id_produto, quantidade, custo, venda, data)

                custo_total_confirmado += custo
                venda_total_confirmada += venda

            if custo_total_confirmado != custo_total or venda_total_confirmada != venda_total:
                raise ValueError("O custo total ou a venda total não conferem com os valores informados")

            conn.commit()

        except ValueError as e:
            conn.rollback()
            raise e

        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()



class Venda:
    def __init__(self, id_venda: int):
        self.id: int = id_venda
        self.custo: float = None
        self.venda: float = None
        self.lucro: float = None
        self.data = None
        self._produtos = []

        self._get_Venda()
        self._get_produtos()

    def _get_Venda(self):
        try:
            banco = Data_Base("database")
            conn = banco.conectar_Banco()
            cursor = conn.cursor()
        
            cursor.execute("""
                SELECT Custo, Venda, Data
                FROM tbVenda
                where idVenda = ?
                """, (self.id, ))
            venda = cursor.fetchall()

            if venda:
                self.custo = venda[0][0]
                self.venda = venda[0][1]
                self.lucro = lucro(self.custo, self.venda)
                self.data = venda[0][2]
                
            else:
                raise ValueError ("Id de venda inexistente")
            
        except ValueError as e:
            raise e

        except Exception as e:
            raise e
        
        finally:
            cursor.close()
            conn.close()


    def _get_produtos(self):
        try:
            banco = Data_Base("database")
            conn = banco.conectar_Banco()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT idVendaProduto, idProduto, Quantidade, Custo, Venda
                FROM tbVendaProduto
                where idVenda = ?
                """, (self.id, ))
            produtos = cursor.fetchall()

            if produtos:
                for produto in produtos:
                    produto_venda = Produto_Venda(produto[0])
                    produto_venda.id_produto = produto[1]
                    produto_venda.quantidade = produto[2]
                    produto_venda.custo = produto[3]
                    produto_venda.venda = produto[4]
                    produto_venda.lucro = lucro(produto_venda.custo, produto_venda.venda)
                    self.produtos.append(produto_venda)

        except Exception as e:
            raise e
        
        finally:
            cursor.close()
            conn.close()



class Produto_Venda:
    def __init__(self, id_produto_venda: int):
        self.id: int = id_produto_venda
        self.id_venda: int = None
        self.id_produto: int = None
        self.quantidade: int = None
        self.custo: float = None
        self.venda: float = None
        self.lucro: float = None
        self.data = None
        
        self._get_Produto_Venda()
    
    def _get_Produto_Venda(self):
        try:
            banco = Data_Base("database")
            conn = banco.conectar_Banco()
            cursor = conn.cursor()
        
            cursor.execute("""
                SELECT idVenda, idProduto, Quantidade, Custo, Venda, Data
                FROM tbVenda
                where idVenda = ?
                """, (self.Id, ))
            produto_venda = cursor.fetchall()

            if produto_venda:
                self.id_venda = produto_venda[0][0]
                self.id_produto = produto_venda[0][1]
                self.quantidade = produto_venda[0][2]
                self.custo = produto_venda[0][3]
                self.venda = produto_venda[0][4]
                self.lucro = lucro(self.custo, self.venda)
                self.data = produto_venda[0][5]
                
            else:
                raise ValueError ("Id de venda inexistente")
            
        except ValueError as e:
            raise e

        except Exception as e:
            raise e
        
        finally:
            cursor.close()
            conn.close()