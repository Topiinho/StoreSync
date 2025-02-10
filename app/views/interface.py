import flet as ft
from menuSideBar import create_sidebar

def main(page: ft.Page):
    page.bgcolor = ft.colors.GREY_800

    sidebar, toggle_sidebar = create_sidebar(page)

    layout = ft.Container(
        content=ft.Row(
            controls=[
                sidebar,
                ft.Container(expand=True, bgcolor=ft.colors.GREY_700),
            ]
        )
    )

    sidebar.on_hover = toggle_sidebar

    page.add(layout)

ft.app(target=main, assets_dir="assets")
