import flet as ft
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.controllers.controleProduto import productList

def foto(foto):
    try:
        foto = ft.Image(src=foto, height=120, width=120, border_radius=20)
        return foto
    except Exception as e:
        raise e

Foto = foto(productList()[0][4])

# def nome(nome):
#     try:
#         nome = ft.Text(nome, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_50)
#         return nome
#     except Exception as e:
#         raise e

# Nome = nome(productList()[0][0])


# def main(page: ft.Page):
#     page.bgcolor = ft.Colors.GREY_900
#     page.padding = 0
#     page.window_width = 1200
#     page.window_height = 800
#     page.window_resizable = True

#     Test = ft.Image(src=Foto, height=120, width=120, border_radius=20)


#     page.add(Test)
#     page.update()


# ft.app(target=main, assets_dir="assets")


def exibir_produtos(page):
    try:
        produtos = productList()

        for produto in produtos:
            nome = produto[0]
            modelo = produto[1]
            custo = produto[2]
            estoque = produto[3]
            foto_base64 = produto[4]

            img_src = f"data:image/png;base64,{foto_base64}"
            img = ft.Image(src=img_src)

            page.add(ft.Text(nome))
            page.add(ft.Text(modelo))
            page.add(ft.Text(f"Custo: {custo}"))
            page.add(ft.Text(f"Estoque: {estoque}"))
            page.add(img)

        page.update()

    except Exception as e:
        page.add(ft.Text(f"Erro ao exibir produtos: {str(e)}"))

ft.app(target=exibir_produtos)




