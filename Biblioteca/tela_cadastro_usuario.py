from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
import requests


class CadastroUsuarioLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(CadastroUsuarioLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [100, 50, 100, 50]  # left, top, right, bottom
        self.spacing = 20

        self.add_widget(Label(text='Nome de usuário:', size_hint_y=None, height=30))
        self.username = TextInput(multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.username)

        self.add_widget(Label(text='Senha:', size_hint_y=None, height=30))
        self.password = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.password)

        self.add_widget(Label(text='Admin:', size_hint_y=None, height=30))
        self.admin_checkbox = CheckBox(active=False, size_hint_y=None, height=40)
        self.add_widget(self.admin_checkbox)



        self.registrar_button = Button(text='Registrar', size_hint_y=None, height=50)
        self.registrar_button.bind(on_press=self.verificar_e_registrar)
        self.add_widget(self.registrar_button)

        # Adicionando label para acessar a tela de login
        self.label_login = Label(text='Já tem cadastro? Clique aqui para voltar ao login!',
                                 color=[0, 0, 1, 1], halign='center', markup=True, size_hint_y=None, height=30)
        self.label_login.bind(on_touch_down=self.ir_para_login)
        self.add_widget(self.label_login)

    def verificar_e_registrar(self, instance):
        nome = self.username.text
        senha = self.password.text
        admin = int(self.admin_checkbox.active)

        # Verificar se os campos de nome de usuário e senha não estão vazios
        if not nome or not senha:
            self.mostrar_popup('Erro', 'Nome de usuário e senha não podem estar vazios!')
            return

        try:
            # Verificar se o usuário já existe
            response = requests.get(f'http://127.0.0.1:5000/usuarios/{nome}')
            if response.status_code == 200:
                self.mostrar_popup('Erro', 'Nome de usuário já existe!')
            elif response.status_code == 404:
                # Registrar o usuário
                response = requests.post('http://127.0.0.1:5000/usuarios',
                                         json={'nome': nome, 'senha': senha, 'admin': admin})
                if response.status_code == 200:
                    self.mostrar_popup('Sucesso', 'Usuário cadastrado com sucesso!', sucesso=True)
                else:
                    self.mostrar_popup('Erro', 'Erro ao cadastrar usuário!')
            else:
                self.mostrar_popup('Erro', 'Erro ao verificar existência do usuário!')
        except requests.ConnectionError:
            self.mostrar_popup('Erro', 'Erro ao conectar com o servidor.')
        except requests.RequestException as e:
            self.mostrar_popup('Erro', f'Erro ao cadastrar usuário: {str(e)}')

    def mostrar_popup(self, titulo, mensagem, sucesso=False):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=mensagem)
        fechar_button = Button(text='Fechar', size_hint=(None, None), size=(100, 50))
        layout.add_widget(popup_label)
        layout.add_widget(fechar_button)
        popup = Popup(title=titulo, content=layout, size_hint=(None, None), size=(400, 200))
        fechar_button.bind(on_press=popup.dismiss)
        if sucesso:
            popup.bind(on_dismiss=lambda x: self.fechar_popup_e_voltar())
        popup.open()

    def fechar_popup_e_voltar(self):
        # Fecha o popup e volta para a tela de login
        App.get_running_app().root.current = 'realizar_login'

    def ir_para_login(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # Redirecionar para a tela de login
            App.get_running_app().root.current = 'realizar_login'

class TelaCadastroUsuarioScreen(Screen):
    def __init__(self, **kwargs):
        super(TelaCadastroUsuarioScreen, self).__init__(**kwargs)
        self.add_widget(CadastroUsuarioLayout())

    def on_pre_enter(self):
        # Limpar os campos ao entrar na tela de cadastro de usuário
        self.clear_inputs()

    def clear_inputs(self):
        # Encontra todos os TextInput na tela e limpa seus textos
        for widget in self.children[0].children:  # Acessa o primeiro filho que é o CadastroUsuarioLayout
            if isinstance(widget, TextInput):
                widget.text = ''
            elif isinstance(widget, CheckBox):
                widget.active = False

