import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

class VerLivrosScreen(Screen):
    def __init__(self, **kwargs):
        super(VerLivrosScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        btn_listar_livros = Button(text='Listar Livros', size_hint_y=None, height=40)
        btn_listar_livros.bind(on_press=self.listar_livros)

        btn_voltar = Button(text='Voltar', size_hint_y=None, height=40)
        btn_voltar.bind(on_press=self.voltar)

        layout.add_widget(btn_listar_livros)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def listar_livros(self, instance):
        try:
            response = requests.get('http://localhost:5000/listar_livros')
            if response.status_code == 200:
                livros = response.json()['livros']
                self.mostrar_popup_livros(livros)
            else:
                print('Erro ao listar livros:', response.text)
        except requests.RequestException as e:
            print('Erro de conexão:', e)

    def mostrar_popup_livros(self, livros):
        content = BoxLayout(orientation='vertical')
        for livro in livros:
            lbl_livro = Label(text=f"Título: {livro['titulo']}, Autor: {livro['autor']}, Ano de Publicação: {livro['ano_publicacao']}")
            content.add_widget(lbl_livro)

        btn_fechar = Button(text='Fechar', size_hint_y=None, height=30)
        btn_fechar.bind(on_press=self.fechar_popup)

        content.add_widget(btn_fechar)
        self.popup = Popup(title='Lista de Livros', content=content, size_hint=(None, None), size=(400, 400))
        self.popup.open()

    def fechar_popup(self, instance):
        self.popup.dismiss()

    def voltar(self, instance):
        self.manager.current = 'login'

class MinhaApp(App):
    def build(self):
        return VerLivrosScreen()

if __name__ == '__main__':
    MinhaApp().run()
