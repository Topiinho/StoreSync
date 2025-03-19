import flet as ft
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.controllers.controleProduto import Product_Control

UNDEFINED_IMAGE = "app/views/assets/Undefined_Icon.png"

class Product_Menu:
    def __init__(self, page, file_picker):
        self.page = page
        self.file_picker = file_picker
        self.is_creating = False
        self.current_image_display = None
        self.product_cards = []

        # Configurar file picker
        self.file_picker.on_result = self.on_file_selected

    def on_file_selected(self, e):
        if e.files and self.current_image_display:
            self.current_image_display.src = e.files[0].path
            self.page.update()

    def _show_dialog(self, title, content, callback=None):
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[ft.TextButton("OK", on_click=callback or self._close_dialog)]
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _close_dialog(self, e=None):
        if e:
            e.page.overlay[-1].open = False
            self.page.update()
            self.list_products("Todos")

    def _validate_inputs(self, nome, modelo, custo, estoque):
        if not all([nome.strip(), modelo.strip(), custo.strip(), estoque.strip()]):
            return False, "Todos os campos obrigatórios devem ser preenchidos."
        
        try:
            return True, (float(custo), int(estoque))
        except ValueError:
            return False, "Custo deve ser um número decimal e Estoque deve ser um número inteiro."

    def _create_product_card(self, id, nome, modelo, custo, estoque, foto):
        is_editing = False
        image_display = ft.Image(src=foto, height=120, width=120, border_radius=20)
        campos_nao_editaveis = ft.Column(controls=[
            ft.Text(nome, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text(f"Modelo: {modelo}", size=15, color=ft.Colors.WHITE)
        ])

        # Componentes editáveis
        custo_field = ft.TextField(value=f"{custo:.2f}", bgcolor=ft.Colors.GREY_700)
        estoque_field = ft.TextField(value=f"{estoque}", bgcolor=ft.Colors.GREY_700)

        def update_product(e):
            valid, result = self._validate_inputs(nome, modelo, custo_field.value, estoque_field.value)
            if not valid:
                self._show_dialog("Erro", result)
                return

            try:
                Product_Control.atualiza_Cadastro(id, nome, modelo, *result, image_display.src)
                self._show_dialog("Sucesso", "Produto atualizado com sucesso!", self._close_dialog)
                toggle_edit_mode()
            except Exception as error:
                self._show_dialog("Erro", f"Ocorreu um erro: {error}")

        def toggle_edit_mode(e=None):
            nonlocal is_editing
            is_editing = not is_editing

            new_content = card_edit if is_editing else card_display
            card.content = new_content
            self.page.update()

        # Card de visualização
        card_display = ft.Row(controls=[
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

        # Card de edição
        card_edit = ft.Row(controls=[
            ft.Container(
                content=image_display,
                on_click=lambda e: setattr(self, 'current_image_display', image_display) or self.file_picker.pick_files()
            ),
            ft.Column(controls=[
                campos_nao_editaveis,
                ft.Row([custo_field, estoque_field])
            ], expand=True),
            ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda e: toggle_edit_mode()),
            ft.IconButton(icon=ft.Icons.SAVE, icon_color=ft.Colors.GREEN, on_click=update_product)
        ])

        card = ft.Container(
            padding=10,
            bgcolor=ft.Colors.GREY_800,
            border_radius=30,
            height=150,
            content=card_display
        )

        return card

    def _create_new_card(self):
        if self.is_creating:
            return
        self.is_creating = True

        image_display = ft.Image(src=UNDEFINED_IMAGE, height=120, width=120, border_radius=20)
        fields = {
            'nome': ft.TextField(label="Nome do Produto", bgcolor=ft.Colors.GREY_700),
            'modelo': ft.TextField(label="Modelo", bgcolor=ft.Colors.GREY_700),
            'custo': ft.TextField(label="Custo", bgcolor=ft.Colors.GREY_700),
            'estoque': ft.TextField(label="Estoque", bgcolor=ft.Colors.GREY_700)
        }

        def confirm_product(e):
            valid, result = self._validate_inputs(
                fields['nome'].value,
                fields['modelo'].value,
                fields['custo'].value,
                fields['estoque'].value
            )
            
            if not valid:
                self._show_dialog("Erro", result)
                return

            try:
                Product_Control.novo_Cadastro(
                    fields['nome'].value.strip(),
                    fields['modelo'].value.strip(),
                    *result,
                    image_display.src
                )
                self._show_dialog("Sucesso", "Produto cadastrado com sucesso!", self._close_dialog)
            except Exception as error:
                self._show_dialog("Erro", f"Ocorreu um erro: {error}")

        new_card = ft.Container(
            padding=10,
            bgcolor=ft.Colors.GREY_800,
            border_radius=30,
            height=180,
            content=ft.Row(controls=[
                ft.Container(
                    content=image_display,
                    on_click=lambda e: setattr(self, 'current_image_display', image_display) or self.file_picker.pick_files()
                ),
                ft.Column(controls=[
                    fields['nome'], 
                    fields['modelo'],
                    ft.Row([fields['custo'], fields['estoque']])
                ], expand=True),
                ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda _: self.remove_product(new_card)),
                ft.IconButton(icon=ft.Icons.CHECK, icon_color=ft.Colors.GREEN, on_click=confirm_product)
            ])
        )

        self.product_list.content.controls.insert(0, new_card)
        self.page.update()

    def remove_product(self, card):
        self.product_list.content.controls.remove(card)
        self.is_creating = False
        self.page.update()

    def list_products(self, filtro):
        self.product_list.content.controls.clear()
        self.is_creating = False

        for produto in Product_Control.product_List(filtro):
            self.product_list.content.controls.append(
                self._create_product_card(*produto)
            )
        
        self.page.update()

    def create_product_menu(self):
        try:
            # Componentes da UI
            self.product_list = ft.Container(
                expand=True,
                content=ft.Column(scroll="auto", expand=True)
            )
            
            campo_pesquisa = ft.TextField(
                label="Pesquisar", 
                hint_text="Digite sua busca...", 
                border_radius=30,
                on_submit=lambda e: self.list_products(campo_pesquisa.value.strip())
            )

            top_bar = ft.Container(
                padding=10,
                bgcolor=ft.Colors.GREY_800,
                border_radius=30,
                content=ft.Row(controls=[
                    campo_pesquisa,
                    ft.ElevatedButton("Buscar", height=50, width=75,
                                     on_click=lambda _: self.list_products(campo_pesquisa.value.strip())),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.REFRESH, on_click=lambda _: self.list_products("Todos")),
                    ft.ElevatedButton(
                        "Novo Cadastro",
                        bgcolor=ft.Colors.GREEN_500,
                        height=50,
                        color=ft.Colors.BLACK,
                        on_click=lambda _: self._create_new_card()
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )

            # Carregar dados iniciais
            self.list_products("Todos")

            return ft.Container(
                expand=True,
                padding=10,
                content=ft.Column(controls=[top_bar, self.product_list], expand=True)
            )
        
        except Exception as e:
            self._show_dialog("Erro", str(e))


# def main(page: ft.Page):
#     page.bgcolor = ft.Colors.GREY_900
#     page.padding = 0
#     page.window_width = 1200
#     page.window_height = 800
#     page.window_resizable = True

#     file_picker = ft.FilePicker()
#     page.overlay.append(file_picker)

#     product_menu = Product_Menu(page, file_picker)
#     page.add(product_menu.create_product_menu())
#     page.update()


# ft.app(target=main, assets_dir="assets")