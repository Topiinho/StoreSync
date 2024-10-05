from app.models.Produto import listar_produtos
from app.models.Produto import cadastrar_produto

cadastrar_produto("Johnny", "Tom", 24, 13, "1", "1")
cadastrar_produto("Addie", "Jesse", 18, 10, "1", "1")
cadastrar_produto("Fannie", "Hattie", 18, 37, "1", "1")
cadastrar_produto("Jacob", "Rosalie", 4, 50, "5", "1")

listar_produtos("Todos", "a")
