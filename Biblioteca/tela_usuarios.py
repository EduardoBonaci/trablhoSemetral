import requests
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class ListaUsuariosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(self.layout)

        self.label_titulo = Label(text='Lista de Usuários', font_size='24sp')
        self.layout.add_widget(self.label_titulo)

        self.btn_atualizar = Button(text='Atualizar Lista')
        self.btn_atualizar.bind(on_press=self.atualizar_lista)
        self.layout.add_widget(self.btn_atualizar)

    def atualizar_lista(self, instance):
        response = requests.get('http://localhost:5000/listar_usuarios')
        if response.status_code == 200:
            usuarios = response.json()
            self.layout.clear_widgets()
            self.layout.add_widget(self.label_titulo)
            self.layout.add_widget(self.btn_atualizar)
            for usuario in usuarios:
                nome = usuario['nome']
                senha = usuario['senha']
                admin = 'Sim' if usuario['admin'] else 'Não'
                label_usuario = Label(text=f'Nome: {nome}, Senha: {senha}, Admin: {admin}')
                self.layout.add_widget(label_usuario)
        else:
            popup = Popup(title='Erro',
                          content=Label(text='Erro ao carregar lista de usuários!'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
