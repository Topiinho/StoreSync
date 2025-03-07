import flet as ft
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.controllers.controleProduto import productList, novoCadastro

is_creating = False  # Variável de controle

Unknown = "app/views/assets/Unknown_Icon.png"

def create_product_menu(page):
    global is_creating  
    product_cards = []

    try:
        # Defina a variável image_display antes de usá-la
        image_display = ft.Image(src=Unknown, height=120, width=120, border_radius=20)

        def on_file_selected(e):
            if e.files and image_display:
                image_display.src = e.files[0].path
                page.update()

        file_picker = ft.FilePicker(on_result=on_file_selected)

        page.add(file_picker)

        def remove_product_card(card):
            global is_creating
            product_cards.remove(card)
            product_list.content.controls.remove(card)
            is_creating = False  # Libera a criação de um novo card
            page.update()

        def create_new_card():
            global is_creating
            if is_creating:
                return

            is_creating = True

            # Criação do card com image_display já acessível
            image_container = ft.Container(
                content=image_display,
                on_click=lambda e: file_picker.pick_files()
            )

            nome_field = ft.TextField(label="Nome do Produto", bgcolor=ft.Colors.GREY_700)
            modelo_field = ft.TextField(label="Modelo", bgcolor=ft.Colors.GREY_700)
            custo_field = ft.TextField(label="Custo", bgcolor=ft.Colors.GREY_700)
            estoque_field = ft.TextField(label="Estoque", bgcolor=ft.Colors.GREY_700)

            def confirmar_novo_produto(e):
                page = e.page  # Pegando a referência da página

                if not nome_field.value.strip() or not modelo_field.value.strip() or not custo_field.value.strip() or not estoque_field.value.strip():
                    erro_dialog = ft.AlertDialog(
                        title=ft.Text("Erro"),
                        content=ft.Text("Todos os campos obrigatórios devem ser preenchidos."),
                        actions=[ft.TextButton("OK", on_click=lambda _: fechar_dialog(erro_dialog, page))],
                    )
                    page.overlay.append(erro_dialog)  # Adiciona o pop-up corretamente
                    erro_dialog.open = True
                    page.update()
                    return

                try:
                    custo = float(custo_field.value)
                    estoque = int(estoque_field.value)
                except ValueError:
                    erro_dialog = ft.AlertDialog(
                        title=ft.Text("Erro"),
                        content=ft.Text("Custo deve ser um número decimal e Estoque deve ser um número inteiro."),
                        actions=[ft.TextButton("OK", on_click=lambda _: fechar_dialog(erro_dialog, page))],
                    )
                    page.overlay.append(erro_dialog)
                    erro_dialog.open = True
                    page.update()
                    return

                try:
                    novoCadastro(
                        nome_field.value.strip(),
                        modelo_field.value.strip(),
                        custo,
                        estoque,
                        image_display.src
                    )

                    sucesso_dialog = ft.AlertDialog(
                        title=ft.Text("Sucesso"),
                        content=ft.Text("Produto cadastrado com sucesso!"),
                        actions=[ft.TextButton("OK", on_click=lambda _: fechar_dialog(sucesso_dialog, page))],
                    )
                    page.overlay.append(sucesso_dialog)
                    sucesso_dialog.open = True
                    page.update()

                    remove_product_card(new_card)  # Remove o card de criação após sucesso

                    image_display.src = Unknown  # Reseta a imagem para a padrão

                except Exception as error:
                    erro_dialog = ft.AlertDialog(
                        title=ft.Text("Erro"),
                        content=ft.Text(f"Ocorreu um erro: {error}"),
                        actions=[ft.TextButton("OK", on_click=lambda _: fechar_dialog(erro_dialog, page))],
                    )
                    page.overlay.append(erro_dialog)
                    erro_dialog.open = True
                    page.update()

            # Função auxiliar para fechar o pop-up
            def fechar_dialog(dialog, page):
                dialog.open = False
                page.update()

            new_card = ft.Container(
                padding=10,
                bgcolor=ft.Colors.GREY_800,
                border_radius=30,
                height=180,
                content=ft.Row(controls=[  
                    image_container,
                    ft.Column(controls=[  
                        nome_field, modelo_field,
                        ft.Row([custo_field, estoque_field]),
                    ], expand=True),
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda _: remove_product_card(new_card)),
                    ft.IconButton(icon=ft.Icons.CHECK, icon_color=ft.Colors.GREEN, on_click=confirmar_novo_produto)
                ])
            )

            product_cards.insert(0, new_card)
            product_list.content.controls.insert(0, new_card)
            page.update()

        def create_product_card(nome, modelo, custo, estoque, foto):
            print(f"Nome: {nome}, Modelo: {modelo}, Custo: {custo}, Estoque: {estoque}, Foto: {foto}") # Debug
            return ft.Container(
                padding=10,
                bgcolor=ft.Colors.GREY_800,
                border_radius=30,
                height=150,
                content=ft.Row(controls=[  
                    ft.Image(src=f"data:image/png;base64,{foto}", height=120, width=120, border_radius=20),
                    ft.Column(controls=[  
                        ft.Text(nome, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(f"Modelo: {modelo}", size=15, color=ft.Colors.WHITE),
                        ft.Row([  
                            ft.Text(f"Custo: R$ {custo:.2f}", size=15, color=ft.Colors.WHITE),
                            ft.Text(f"Estoque: {estoque}", size=15, color=ft.Colors.WHITE)
                        ])
                    ], expand=True),
                    ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE)  # Agora está azul
                ])
            )

        product_list_data = productList()
        for produto in product_list_data:
            product_card = create_product_card(*produto)
            product_cards.append(product_card)

        product_list = ft.Container(
            padding=10,
            expand=True,
            content=ft.Column(controls=product_cards, scroll="auto", expand=True)
        )

        top_bar = ft.Container(
            padding=10,
            bgcolor=ft.Colors.GREY_800,
            border_radius=30,
            content=ft.Row(
                controls=[  
                    ft.TextField(label="Pesquisar", hint_text="Digite sua busca...", border_radius=30),
                    ft.ElevatedButton("Buscar", height=50, width=75),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.REFRESH),
                    ft.ElevatedButton(
                        "Novo Cadastro",
                        bgcolor=ft.Colors.GREEN_500,
                        height=50,
                        color=ft.Colors.BLACK,
                        on_click=lambda _: create_new_card()
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

        product_menu = ft.Container(
            expand=True,
            padding=10,
            content=ft.Column(controls=[top_bar, product_list], expand=True),
        )

        return product_menu
    except Exception as e:
        raise e





def main(page: ft.Page):
    page.bgcolor = ft.Colors.GREY_900
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800
    page.window_resizable = True

    productMenu = create_product_menu(page)

    page.add(productMenu)
    page.update()


ft.app(target=main, assets_dir="assets")
