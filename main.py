import subprocess

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button




class MyApp(App):

    def build(self):


        self.iniciar_servidor_flask()
        layout = BoxLayout(orientation='vertical', size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})

        lbl_usuario = Label(text='Usuário')
        txt_usuario = TextInput(multiline=False, size_hint_y=None, height=30)
        layout.add_widget(lbl_usuario)
        layout.add_widget(txt_usuario)

        lbl_senha = Label(text='Senha')
        txt_senha = TextInput(text='', multiline=False, size_hint_y=None, height=30)
        layout.add_widget(lbl_senha)
        layout.add_widget(txt_senha)

        lbl_cadastro = Label(text='Não tem cadastro? Clique aqui')
        lbl_cadastro.bind(on_touch_down=self.on_label_pressed)
        btn_login = Button(text='Login', size_hint_y=None, height=30)


        layout.add_widget(lbl_cadastro)
        layout.add_widget(btn_login)

        return layout

    def iniciar_servidor_flask(self):
        # Comando para iniciar o servidor Flask
        comando = 'python  backend.py run --host=0.0.0.0 '
        try:
            # Executar o comando em segundo plano usando subprocess
            subprocess.Popen(comando, shell=True)
        except Exception as e:
            print('Erro ao iniciar o servidor Flask:', e)
    def on_label_pressed(self, instance, touch):
        self.root.clear_widgets()
        if instance.collide_point(*touch.pos):
            from tela_cadastro_usuario import CadastroUsuario


            self.root.add_widget(CadastroUsuario().build())

   # def on_login_pressed(self, instance):



if __name__ == '__main__':
    MyApp().run()
