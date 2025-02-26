import flet as ft

def create_sidebar(page):
    sidebar_expanded = False

    def toggle_sidebar(e):
        nonlocal sidebar_expanded
        sidebar_expanded = not sidebar_expanded
        sidebar.width = 150 if sidebar_expanded else 70
        for button in menu_buttons:
            button.content.controls[1].visible = sidebar_expanded  # Mostrar ou esconder os textos
        config_button.content.controls[1].visible = sidebar_expanded
        page.update()

    menu_buttons = [
        ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.icons.HOME),
                ft.Text("Menu Inicial", visible=False)
            ])
        ),

        ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.icons.SHOPPING_CART),
                ft.Text("Produtos", visible=False)
            ])
        ),

        ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.icons.MONETIZATION_ON),
                ft.Text("Vendas", visible=False)
            ])
        ),

        ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.icons.RECEIPT_LONG),
                ft.Text("Compras", visible=False)
            ])
        ),

        ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.icons.SUPPORT_AGENT),
                ft.Text("Fornecedor", visible=False)
            ])
        )
    ]

    config_button = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.icons.SETTINGS),
                ft.Text("Configuração", visible=False),
            ]
        ),
        on_click=...
    )

    sidebar = ft.Container(
        margin=0,
        width=70,
        bgcolor= "#315c77" ,
        border_radius=ft.BorderRadius(top_left=0, top_right=20, bottom_left=0, bottom_right=20),
        padding=10,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    padding=5,
                    content=ft.Image(src="Sync_Logo.png", width=50, height=50),
                    bgcolor=ft.colors.WHITE,
                    shape=ft.BoxShape.CIRCLE,
                    alignment=ft.alignment.top_center
                ),


                ft.Divider(),

                ft.Column(
                    controls=menu_buttons,
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Container(expand=True),

                ft.Divider(),


                config_button
            ]
        )
    )
    
    return sidebar, toggle_sidebar
