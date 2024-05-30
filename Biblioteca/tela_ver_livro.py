# tela_ver_livros.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import requests

class VerLivrosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.btn_atualizar = Button(text='Atualizar Lista de Livros')
        self.btn_atualizar.bind(on_press=self.listar_livros)
        self.layout.add_widget(self.btn_atualizar)

        self.btn_voltar = Button(text='Voltar')
        self.btn_voltar.bind(on_press=self.voltar)
        self.layout.add_widget(self.btn_voltar)

    def listar_livros(self, instance):
        try:
            response = requests.get('http://localhost:5000/listar_livros')
            if response.status_code == 200:
                livros = response.json()
                for livro in livros:
                    lbl_livro = Label(text=f"Título: {livro['titulo']}, Autor: {livro['autor']}")
                    self.layout.add_widget(lbl_livro)
            else:
                print(response.text)
        except requests.RequestException as e:
            print('Erro de conexão:', e)

    def voltar(self, instance):
        self.manager.current = 'lista'

if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(VerLivrosScreen())
