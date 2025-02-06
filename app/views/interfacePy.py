from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class MainScreen(BoxLayout):
    pass

class StoreSyncApp(App):
    def build(self):
        self.title = "StoreSync"
        Builder.load_file('interfaceKv.kv')
        return MainScreen()

    def on_start(self):
        print("Aplicativo iniciado com sucesso!")

if __name__ == '__main__':
    StoreSyncApp().run()
