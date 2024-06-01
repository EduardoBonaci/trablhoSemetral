from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.screenmanager import Screen

import requests

class LoginScreenLayout(Screen):
    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=100, spacing=20)

        scrollview = ScrollView()
        scrollview.add_widget(layout)

        self.add_widget(scrollview)

        layout.add_widget(Label(text='Nome de usuário:', size_hint=(1, None), height=30))
        self.username = TextInput(multiline=False, hint_text='Digite seu nome de usuário')
        layout.add_widget(self.username)

        layout.add_widget(Label(text='Senha:', size_hint=(1, None), height=30))
        self.password = TextInput(password=True, multiline=False, hint_text='Digite sua senha')
        layout.add_widget(self.password)

        self.login_button = Button(text='Login', size_hint=(1, None), height=50)
        self.login_button.bind(on_press=self.fazer_login)
        layout.add_widget(self.login_button)

        self.registrar_label = Label(text='Ainda não tem uma conta? Clique aqui para se registrar!',
                                     size_hint=(1, None), height=50, color=(0, 0.5, 1, 1), markup=True)
        self.registrar_label.bind(on_touch_down=self.ir_para_registro)
        layout.add_widget(self.registrar_label)

    def fazer_login(self, instance):
        nome = self.username.text
        senha = self.password.text

        # Verificar se os campos de nome de usuário e senha não estão vazios
        if not nome or not senha:
            self.mostrar_popup('Erro', 'Nome de usuário e senha não podem estar vazios!')
            return

        try:
            response = requests.post('http://127.0.0.1:5000/login', json={'nome': nome, 'senha': senha})
            if response.status_code == 200:
                data = response.json()
                app = App.get_running_app()
                if data.get('admin') == 1:
                    app.root.current = 'administrador'
                else:
                    app.root.current = 'tela_usuario'  # Mudança aqui
            else:
                self.mostrar_popup('Erro', 'Usuário ou senha incorretos!')
        except requests.ConnectionError:
            self.mostrar_popup('Erro', 'Erro ao conectar com o servidor.')
        except requests.RequestException as e:
            self.mostrar_popup('Erro', f'Erro ao realizar login: {str(e)}')

    def mostrar_popup(self, titulo, mensagem):
        # Verifica se a tela atual é a tela de login antes de exibir o popup
        if App.get_running_app().root.current == 'realizar_login':
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            popup_label = Label(text=mensagem)
            fechar_button = Button(text='Fechar', size_hint=(None, None), size=(100, 50))
            layout.add_widget(popup_label)
            layout.add_widget(fechar_button)
            popup = Popup(title=titulo, content=layout, size_hint=(None, None), size=(400, 200))
            fechar_button.bind(on_press=popup.dismiss)
            popup.bind(on_dismiss=self.popup_dismissed)  # Adiciona evento on_dismiss
            popup.open()

    def popup_dismissed(self, instance):
        pass

    def mostrar_mensagem(self, titulo, mensagem):
        popup = Popup(title=titulo, content=Label(text=mensagem), size_hint=(None, None), size=(300, 200))
        popup.open()

    def ir_para_registro(self, instance, touch):
        if instance.collide_point(*touch.pos):
            app = App.get_running_app()
            app.root.current = 'cadastrar_usuario'
