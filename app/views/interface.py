import flet as ft
from menuSideBar import create_sidebar
from menuProdutos import Product_menu

def main(page: ft.Page):
    page.bgcolor = "#7c7c7c"
    page.padding = 0

    # Definir um tamanho inicial da janela, mas permitir redimensionamento
    page.window_width = 1200
    page.window_height = 800
    page.window_resizable = True  # Permite que o usuário ajuste a tela

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)


    sidebar, toggle_sidebar = create_sidebar(page)
    productMenu = Product_menu(page, file_picker)


    layout = ft.Row(
        controls=[
            sidebar,
            productMenu.create_product_menu(),
        ],
        expand=True,
    )

    sidebar.on_hover = toggle_sidebar

    page.add(layout)
    # page.update()  # Garante que os ajustes sejam aplicados

ft.app(target=main, assets_dir="assets")
