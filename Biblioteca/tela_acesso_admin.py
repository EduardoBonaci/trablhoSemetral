from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import requests
from kivy.app import App

class AcessoAdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AcessoAdminScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()  # Limpar widgets ao construir a UI
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        btn_listar_usuarios = Button(text='Listar Usuários', size_hint_y=None, height=40)
        btn_listar_usuarios.bind(on_press=self.listar_usuarios)
        layout.add_widget(btn_listar_usuarios)

        btn_cadastrar_livros = Button(text='Cadastrar Livros', size_hint_y=None, height=40)
        btn_cadastrar_livros.bind(on_press=self.cadastrar_livros)
        layout.add_widget(btn_cadastrar_livros)

        btn_ver_livros = Button(text='Ver Livros', size_hint_y=None, height=40)
        btn_ver_livros.bind(on_press=self.ver_livros)
        layout.add_widget(btn_ver_livros)

        btn_voltar = Button(text='Voltar', size_hint_y=None, height=40)
        btn_voltar.bind(on_press=self.voltar)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def listar_usuarios(self, instance):
        try:
            response = requests.get('http://127.0.0.1:5000/usuarios')
            if response.status_code == 200:
                usuarios = response.json()
                self.display_usuarios(usuarios)
            else:
                self.mostrar_popup('Erro', 'Erro ao listar usuários!')
        except requests.ConnectionError:
            self.mostrar_popup('Erro', 'Erro de conexão ao listar usuários.')

    def display_usuarios(self, usuarios):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        scroll_view = ScrollView()
        grid_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Cabeçalhos
        grid_layout.add_widget(Label(text='Usuário', bold=True, size_hint_y=None, height=40))
        grid_layout.add_widget(Label(text='Admin', bold=True, size_hint_y=None, height=40))

        for usuario in usuarios:
            usuario_label = Label(text=usuario['nome'], size_hint_y=None, height=40)
            admin_label = Label(text='Sim' if usuario['admin'] else 'Não', size_hint_y=None, height=40)
            grid_layout.add_widget(usuario_label)
            grid_layout.add_widget(admin_label)

        scroll_view.add_widget(grid_layout)
        layout.add_widget(scroll_view)

        btn_voltar = Button(text='Voltar', size_hint_y=None, height=40)
        btn_voltar.bind(on_press=self.voltar_para_acesso_admin)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def cadastrar_livros(self, instance):
        app = App.get_running_app()
        app.root.current = 'cadastro_livros'

    def ver_livros(self, instance):
        try:
            response = requests.get('http://127.0.0.1:5000/listar_livros')
            if response.status_code == 200:
                livros = response.json()
                self.display_livros(livros)
            else:
                self.mostrar_popup('Erro', 'Erro ao listar livros!')
        except requests.ConnectionError:
            self.mostrar_popup('Erro', 'Erro de conexão ao listar livros.')

    def display_livros(self, data):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        livros = data.get('livros', [])
        scroll_view = ScrollView()
        grid_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Cabeçalhos
        grid_layout.add_widget(Label(text='Título', bold=True, size_hint_y=None, height=40))
        grid_layout.add_widget(Label(text='Autor', bold=True, size_hint_y=None, height=40))
        grid_layout.add_widget(Label(text='Ano de Publicação', bold=True, size_hint_y=None, height=40))

        for livro in livros:
            titulo_label = Label(text=livro.get('titulo', ''), size_hint_y=None, height=40)
            autor_label = Label(text=livro.get('autor', ''), size_hint_y=None, height=40)
            ano_label = Label(text=str(livro.get('ano_publicacao', '')), size_hint_y=None, height=40)
            grid_layout.add_widget(titulo_label)
            grid_layout.add_widget(autor_label)
            grid_layout.add_widget(ano_label)

        scroll_view.add_widget(grid_layout)
        layout.add_widget(scroll_view)

        btn_voltar = Button(text='Voltar', size_hint_y=None, height=40)
        btn_voltar.bind(on_press=self.voltar_para_acesso_admin)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def voltar(self, instance):
        app = App.get_running_app()
        app.root.current = 'realizar_login'

    def voltar_para_acesso_admin(self, instance):
        self.clear_widgets()
        self.build_ui()
        app = App.get_running_app()
        app.root.current = 'acesso_admin'

    def mostrar_popup(self, titulo, mensagem):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=mensagem)
        fechar_button = Button(text='Fechar', size_hint=(None, None), size=(100, 50))
        layout.add_widget(popup_label)
        layout.add_widget(fechar_button)
        popup = Popup(title=titulo, content=layout, size_hint=(None, None), size=(400, 200))
        fechar_button.bind(on_press=popup.dismiss)
        popup.open()
