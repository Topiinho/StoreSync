import flet as ft

def creat_product_menu(page):


    # Barra superior com pesquisa e filtro
    top_bar = ft.Container(
        padding=10,
        bgcolor=ft.colors.GREY_800,
        border_radius=30,
        content=ft.Row(
            controls=[
                ft.TextField(
                    label="Pesquisar",
                    hint_text="Digite sua busca...",
                    border_radius=30,
                ),

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

                ft.Container(expand=True),  # Espaço entre os elementos

                ft.ElevatedButton(
                    "Novo Cadastro",
                    bgcolor=ft.colors.GREEN_500,
                    height=50,
                    color=ft.colors.BLACK,
                    ),

            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Distribui melhor os elementos
        )
    )

    productMenu = ft.Container(
        expand=True,
        padding=10,
        content=ft.Column(
            controls=[top_bar],
            expand=True
        ),
    )

    return productMenu
