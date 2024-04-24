import subprocess
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class CadastroUsuario(App):
    def build(self):

        self.Janela_cadastro = BoxLayout(orientation='vertical', size_hint=(.5, .5),
                                         pos_hint={'center_x': .5, 'center_y': .5})

        lbl_usuario = Label(text='Nome de Usuário')
        self.txt_usuario = TextInput(multiline=False, size_hint_y=None, height=30)
        self.Janela_cadastro.add_widget(lbl_usuario)
        self.Janela_cadastro.add_widget(self.txt_usuario)

        lbl_senha = Label(text='Crie uma Senha')
        self.txt_senha = TextInput(text='', multiline=False, size_hint_y=None, height=30)
        self.Janela_cadastro.add_widget(lbl_senha)
        self.Janela_cadastro.add_widget(self.txt_senha)

        lbl_aviso = Label(text='', color=(1, 0, 0, 1))  # Label para exibir aviso em vermelho
        self.Janela_cadastro.add_widget(lbl_aviso)

        lbl_cadastro = Label(text='Ja tem cadastro? Clique aqui' )
        btn_cadastrar = Button(text='Cadastrar', size_hint_y=None, height=30)
        btn_cadastrar.bind(on_press=self.cadastrar_usuario)
        check_user_admin = CheckBox()
        self.Janela_cadastro.add_widget(lbl_cadastro)
        self.Janela_cadastro.add_widget(check_user_admin)
        self.Janela_cadastro.add_widget(btn_cadastrar)

        self.lbl_aviso = lbl_aviso  # Atribuir o Label de aviso a um atributo da classe para fácil acesso
        return self.Janela_cadastro

    def cadastrar_usuario(self, instance):
        nome_usuario = self.txt_usuario.text
        senha = self.txt_senha.text

        # Verifica se o nome de usuário e a senha foram inseridos
        if not nome_usuario or not senha:
            self.lbl_aviso.text = 'Nome de usuário e senha são obrigatórios!'
        else:
            data = {'nome_usuario': nome_usuario, 'senha': senha}
            try:
                response = requests.post('http://localhost:5000/cadastro', data=data)
                if response.status_code == 200:

                    self.mostrar_popup('Cadastro com sucesso!')


                else:
                    print('Erro ao cadastrar usuário:', response.text)
            except requests.RequestException as e:
                print('Erro de conexão:', e)

    def mostrar_popup(self, message):

        content = BoxLayout(orientation='vertical')
        btn_sair = Button(text='OK')
        btn_sair.bind(on_touch_down=self.abrirMain)
        lbl_mensagem = Label(text=message)

        content.add_widget(lbl_mensagem)
        content.add_widget(btn_sair)
        global popup
        popup = Popup(title='Sucesso', content=content, size_hint=(None, None), size=(400, 200))
        popup.open()


    def abrirMain(self, instance, touch):
        popup.dismiss()
        if instance.collide_point(*touch.pos):
            from main import MyApp

            self.root.add_widget(MyApp().build())



if __name__ == '__main__':
    CadastroUsuario().run()
