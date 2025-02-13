import flet as ft
from menuSideBar import create_sidebar
from menuProdutos import creat_product_menu

def main(page: ft.Page):
    page.bgcolor = "#7c7c7c"

    sidebar, toggle_sidebar = create_sidebar(page)
    productMenu = creat_product_menu(page)

    layout = ft.Row(
        controls=[
            sidebar,
            productMenu,
        ],
        expand=True,

    )

    sidebar.on_hover = toggle_sidebar

    page.add(layout)

ft.app(target=main, assets_dir="assets")
