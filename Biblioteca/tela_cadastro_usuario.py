import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class CadastroUsuarioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(layout)

        self.label_usuario = Label(text='Nome de Usuário')
        self.input_usuario = TextInput()

        self.label_senha = Label(text='Senha')
        self.input_senha = TextInput(password=True)

        self.label_admin = Label(text='Administrador')
        self.spinner_admin = Spinner(text='Não', values=['Sim', 'Não'])

        self.btn_cadastrar = Button(text='Cadastrar')
        self.btn_cadastrar.bind(on_press=self.cadastrar_usuario)

        layout.add_widget(self.label_usuario)
        layout.add_widget(self.input_usuario)
        layout.add_widget(self.label_senha)
        layout.add_widget(self.input_senha)
        layout.add_widget(self.label_admin)
        layout.add_widget(self.spinner_admin)
        layout.add_widget(self.btn_cadastrar)

    def cadastrar_usuario(self, instance):
        nome_usuario = self.input_usuario.text
        senha = self.input_senha.text
        is_admin = 1 if self.spinner_admin.text == 'Sim' else 0

        response = requests.post('http://localhost:5000/cadastro',
                                 data={'nome_usuario': nome_usuario, 'senha': senha, 'is_admin': is_admin})
        if response.status_code == 200:
            self.manager.current = 'lista'
        else:
            popup = Popup(title='Erro',
                          content=Label(text='Erro ao cadastrar usuário!'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
