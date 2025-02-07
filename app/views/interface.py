import flet as ft

def main(page: ft.Page):
    page.bgcolor = ft.colors.GREY_800

    leftSideBarNavi = ft.Container(
        padding=10,
        height=1080,
        border_radius=5,
        col= 1,
        bgcolor= ft.colors.BLUE_GREY_900,
        content=ft.Column(
            controls=[
                ft.Container(
                    padding=1,
                    content=ft.Image(src="Sync_Logo.png"),
                    bgcolor=ft.colors.WHITE,
                    shape=ft.BoxShape.CIRCLE,
                    height= 50,
                    alignment=ft.alignment.center
                )
            ]
        )
    )

    layout = ft.Container(
        width=1920,
        height=1080,
        content=ft.Row(
            controls=[
                leftSideBarNavi,
            ]
        )
    )

    page.add(layout)

ft.app(target=main, assets_dir="assets")