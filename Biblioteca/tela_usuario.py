from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
import requests

class TelaUsuario(Screen):
    def __init__(self, **kwargs):
        super(TelaUsuario, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        lbl_titulo = Label(text='Livros Disponíveis', size_hint_y=None, height=40)
        layout.add_widget(lbl_titulo)

        scroll_view = ScrollView()
        self.grid_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        self.carregar_livros()

        scroll_view.add_widget(self.grid_layout)
        layout.add_widget(scroll_view)

        btn_voltar = Button(text='Voltar', size_hint_y=None, height=40)
        btn_voltar.bind(on_press=self.voltar)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def carregar_livros(self):
        try:
            response = requests.get('http://127.0.0.1:5000/listar_livros')
            if response.status_code == 200:
                livros = response.json().get('livros', [])
                self.display_livros(livros)
            else:
                print('Erro ao listar livros')
        except requests.ConnectionError:
            print('Erro de conexão ao listar livros')

    def display_livros(self, livros):
        self.grid_layout.clear_widgets()

        # Cabeçalhos
        self.grid_layout.add_widget(Label(text='Título', bold=True, size_hint_y=None, height=40))
        self.grid_layout.add_widget(Label(text='Autor', bold=True, size_hint_y=None, height=40))
        self.grid_layout.add_widget(Label(text='Ano de Publicação', bold=True, size_hint_y=None, height=40))

        for livro in livros:
            titulo_label = Label(text=livro.get('titulo', ''), size_hint_y=None, height=40)
            autor_label = Label(text=livro.get('autor', ''), size_hint_y=None, height=40)
            ano_label = Label(text=str(livro.get('ano_publicacao', '')), size_hint_y=None, height=40)
            self.grid_layout.add_widget(titulo_label)
            self.grid_layout.add_widget(autor_label)
            self.grid_layout.add_widget(ano_label)

    def voltar(self, instance):
        self.manager.current = 'realizar_login'  # Altere para o nome correto da tela de login
