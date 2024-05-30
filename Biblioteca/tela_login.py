import subprocess
import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=1, rows=7, spacing=10, size_hint=(None, None), width=400, height=350)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.label_usuario = Label(text='Nome de usuário:', size_hint=(None, None), height=40)
        self.input_usuario = TextInput(size_hint=(None, None), height=40, width=400)

        self.label_senha = Label(text='Senha:', size_hint=(None, None), height=40)
        self.input_senha = TextInput(password=True, size_hint=(None, None), height=40, width=400)

        self.btn_login = Button(text='Login', size_hint=(None, None), height=40, width=400)
        self.btn_login.bind(on_press=self.login)

        self.btn_cadastro = Button(text='Cadastrar', size_hint=(None, None), height=40, width=400)
        self.btn_cadastro.bind(on_press=self.cadastrar)

        self.add_widget(self.layout)
        self.layout.add_widget(self.label_usuario)
        self.layout.add_widget(self.input_usuario)
        self.layout.add_widget(self.label_senha)
        self.layout.add_widget(self.input_senha)
        self.layout.add_widget(self.btn_login)
        self.layout.add_widget(self.btn_cadastro)

    def login(self, instance):
        nome_usuario = self.ids['input_usuario'].text
        senha = self.ids['input_senha'].text
        dados = {'nome_usuario': nome_usuario, 'senha': senha}
        response = requests.post('http://localhost:5000/login', data=dados)
        if response.status_code == 200:
            self.manager.current = 'lista'
        else:
            popup = Popup(title='Erro de Login',
                          content=Label(text='Nome de usuário ou senha incorretos!'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

    def cadastrar(self, instance):
        self.manager.current = 'tela_cadastro_usuario'
