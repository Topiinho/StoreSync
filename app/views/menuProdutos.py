import flet as ft
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.controllers.controleProduto import productList

def create_product_menu(page):

    # Barra superior fixa
    top_bar = ft.Container(
        padding=10,
        bgcolor=ft.Colors.GREY_800,
        border_radius=30,
        content=ft.Row(
            controls=[
                ft.TextField(label="Pesquisar", hint_text="Digite sua busca...", border_radius=30),
                ft.Dropdown(
                    label="Filtrar por tag",
                    options=[
                        ft.dropdown.Option("Eletrônicos"),
                        ft.dropdown.Option("Roupas"),
                        ft.dropdown.Option("Acessórios"),
                        ft.dropdown.Option("Alimentos"),
                    ],
                    border_radius=30,
                    width=150
                ),
                ft.ElevatedButton("Buscar", height=50, width=75),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.icons.REFRESH),
                ft.ElevatedButton(
                    "Novo Cadastro",
                    bgcolor=ft.Colors.GREEN_500,
                    height=50,
                    color=ft.Colors.BLACK,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    # Função para criar um card de produto
    def create_product_card(nome, modelo, custo, estoque, descricao):
        return ft.Container(
            padding=10,
            bgcolor=ft.colors.GREY_800,
            border_radius=30,
            height=150,
            content=ft.Row(controls=[
                # Imagem do produto
                ft.Image(src="app/views/Prototipo de telas/Sem título.png", height=150, border_radius=20),

                # Informações do produto agrupadas
                ft.Column(controls=[
                    # Nome do Produto
                    ft.Container(
                        content=ft.Text(nome, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        bgcolor=ft.colors.GREY_600,
                        border_radius=10,
                        padding=5
                    ),
                    
                    # Modelo
                    ft.Container(
                        content=ft.Text(f"Modelo: {modelo}", size=15, color=ft.colors.WHITE),
                        bgcolor=ft.colors.GREY_600,
                        border_radius=10,
                        padding=5
                    ),

                    # Custo e Estoque em uma linha
                    ft.Row(controls=[
                        ft.Container(
                            content=ft.Text(f"Custo: R$ {custo:.2f}", size=15, color=ft.colors.WHITE),
                            bgcolor=ft.colors.GREY_600,
                            border_radius=10,
                            padding=5
                        ),
                        ft.Container(
                            content=ft.Text(f"Estoque: {estoque}", size=15, color=ft.colors.WHITE),
                            bgcolor=ft.colors.GREY_600,
                            border_radius=10,
                            padding=5
                        )
                    ])
                ]),

                # Descrição com largura mínima
                ft.Container(
                    content=ft.Text(descricao, size=13, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS, color=ft.colors.BLACK),
                    bgcolor=ft.colors.GREY_600,
                    border_radius=10,
                    padding=5,
                    width=200,  # Define uma largura mínima para a descrição
                    height=150,
                ),

                ft.Container(expand=True),

                # Gráfico ou outra imagem
                ft.Image(src="https://educa.ibge.gov.br/images/educa/jovens/materiais-estudo/2018_10_24_exemplo_graf-colunas_animacao.gif", width=300, height=150),

                # Botão de edição
                ft.IconButton(icon=ft.icons.EDIT, icon_color=ft.colors.BLUE)
            ])
    )


    # Criar a lista de produtos dinamicamente
    product_list_data = productList()  # Obtendo os produtos do banco
    product_cards = [create_product_card(*produto) for produto in product_list_data]  # Criando os containers

    # Criar a lista de produtos na UI (com rolagem adaptativa)
    product_list = ft.Container(
        padding=10,
        expand=True,  # Expande para ocupar o espaço restante
        content=ft.Column(controls=product_cards, scroll="auto", expand=True)  # Scroll ativado
    )

    # Estrutura geral do menu
    product_menu = ft.Container(
        expand=True,
        padding=10,
        content=ft.Column(
            controls=[
                top_bar,  # Barra fixa
                product_list  # Lista rolável adaptativa
            ],
            expand=True
        ),
    )

    return product_menu
