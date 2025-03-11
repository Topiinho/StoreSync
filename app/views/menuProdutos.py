import flet as ft
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.controllers.controleProduto import productList, novoCadastro

is_creating = False  # Variável de controle

Undefined = "app/views/assets/Undefined_Icon.png"

def create_product_menu(page):
    global is_creating  
    product_cards = []

    try:
        # Defina a variável image_display antes de usá-la
        image_display = ft.Image(src=Undefined, height=120, width=120, border_radius=20)

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

                    image_display.src = Undefined  # Reseta a imagem para a padrão

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
                list_products("Todos")

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
            is_editing = False

            def Atualizar_produto(e):
                page = e.page  # Pegando a referência da página

                if not custo_field.value.strip() or not estoque_field.value.strip():
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
                        nome,
                        modelo,
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

                    image_display.src = Undefined  # Reseta a imagem para a padrão

                except Exception as error:
                    erro_dialog = ft.AlertDialog(
                        title=ft.Text("Erro"),
                        content=ft.Text(f"Ocorreu um erro: {error}"),
                        actions=[ft.TextButton("OK", on_click=lambda _: fechar_dialog(erro_dialog, page))],
                    )
                    page.overlay.append(erro_dialog)
                    erro_dialog.open = True
                    page.update()


            campos_nao_editaveis = ft.Column(controls=[  
                ft.Text(nome, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(f"Modelo: {modelo}", size=15, color=ft.Colors.WHITE)])
            
            card = ft.Container(
                padding=10,
                bgcolor=ft.Colors.GREY_800,
                border_radius=30,
                height=150,
                content=ft.Row(controls=[  
                    ft.Image(src=foto, height=120, width=120, border_radius=20),
                    ft.Column(controls=[  
                        campos_nao_editaveis,
                        ft.Row([  
                            ft.Text(f"Custo: R$ {custo:.2f}", size=15, color=ft.Colors.WHITE),
                            ft.Text(f"Estoque: {estoque}", size=15, color=ft.Colors.WHITE)
                        ])
                    ], expand=True),
                    ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda _: toggle_edit_mode())
                ])
            )

            image_display = ft.Image(src=foto, height=120, width=120, border_radius=20)

            def change_image(e):
                if e.files:
                    image_display.src = e.files[0].path
                    page.update()

            file_picker_2 = ft.FilePicker(on_result=change_image)

            page.add(file_picker_2)   
            
            image_container = ft.Container(
                content=image_display,
                on_click=lambda e: file_picker_2.pick_files()
            )

            custo_field = ft.TextField(value=f"{custo:.2f}", bgcolor=ft.Colors.GREY_700)
            estoque_field = ft.TextField(value=f"{estoque}", bgcolor=ft.Colors.GREY_700)

            card_on_edit = ft.Container(
                padding=10,
                bgcolor=ft.Colors.GREY_800,
                border_radius=30,
                height=150,
                content=ft.Row(controls=[  
                    image_container,
                    ft.Column(controls=[  
                        campos_nao_editaveis,
                        ft.Row([  
                            custo_field,
                            estoque_field
                        ])
                    ], expand=True),
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda _: remove_product_card(card)),
                    ft.IconButton(icon=ft.Icons.SAVE, icon_color=ft.Colors.GREEN, on_click=Atualizar_produto)
                ])
            )

            # Função auxiliar para fechar o pop-up
            def fechar_dialog(dialog, page):
                dialog.open = False
                page.update()
                list_products("Todos")

            def toggle_edit_mode():
                nonlocal is_editing
                is_editing = not is_editing

                index = product_list.content.controls.index(card)  # Obtém a posição original do card

                if is_editing:
                    product_list.content.controls.pop(index)  # Remove o card original
                    product_list.content.controls.insert(index, card_on_edit)  # Insere o card de edição no mesmo lugar
                else:
                    print("Cancelando edição")
                    product_list.content.controls.pop(index)  # Remove o card editável
                    product_list.content.controls.insert(index, card)  # Insere o card original no mesmo lugar

                page.update()

            
            return card

        def list_products(filtro):
            global is_creating
            if is_creating:
                product_cards.clear()
                product_list.content.controls.clear()
                is_creating = False
                list_products(filtro)
                return

            product_cards.clear()
            product_list.content.controls.clear()

            product_list_data = productList(filtro)
            for produto in product_list_data:
                product_card = create_product_card(*produto)
                product_cards.append(product_card)

            product_list.content.controls.extend(product_cards)
            campoPesquisa.value = ""
            page.update()
            
        product_list_data = productList("Todos")
        for produto in product_list_data:
            product_card = create_product_card(*produto)
            product_cards.append(product_card)


        product_list = ft.Container(
            padding=10,
            expand=True,
            content=ft.Column(controls=product_cards, scroll="auto", expand=True)
        )

        campoPesquisa = ft.TextField(label="Pesquisar", hint_text="Digite sua busca...", border_radius=30)

        top_bar = ft.Container(
            padding=10,
            bgcolor=ft.Colors.GREY_800,
            border_radius=30,
            content=ft.Row(
                controls=[  
                    campoPesquisa,
                    ft.ElevatedButton("Buscar", height=50, width=75, on_click=lambda _: list_products(campoPesquisa.value.strip())),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.REFRESH, on_click=lambda _: list_products("Todos")),
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
