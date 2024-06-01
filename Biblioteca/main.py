import subprocess
import sys

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from tela_login import LoginScreenLayout
from tela_cadastro_usuario import TelaCadastroUsuarioScreen
from tela_acesso_admin import AcessoAdminScreen
from tela_cadastro_livros import CadastroLivroScreen
from tela_ver_livros import VerLivrosScreen
from tela_usuario import TelaUsuario  # Importação da tela de usuário

class GerenciadorTela(ScreenManager):
    def __init__(self, **kwargs):
        super(GerenciadorTela, self).__init__(**kwargs)
        self.add_widget(LoginScreenLayout(name='realizar_login'))
        self.add_widget(TelaCadastroUsuarioScreen(name='cadastrar_usuario'))
        self.add_widget(AcessoAdminScreen(name='administrador'))
        self.add_widget(AcessoAdminScreen(name='acesso_admin'))

        self.add_widget(CadastroLivroScreen(name='cadastro_livros'))
        self.add_widget(VerLivrosScreen(name='ver_livros'))
        self.add_widget(TelaUsuario(name='tela_usuario'))  # Adicionando a tela de usuário

class MainApp(App):
    def build(self):
        self.iniciar_servidor_flask()
        return GerenciadorTela()

    def iniciar_servidor_flask(self):
        comando = [sys.executable, 'backend.py', 'run', '--host=0.0.0.0']
        try:
            subprocess.Popen(comando)
            print('Servidor Flask iniciado com sucesso.')
        except Exception as e:
            print('Erro ao iniciar o servidor Flask:', repr(e))

    def on_stop(self):
        subprocess.Popen(["pkill", "-f", "backend.py"])  # Encerra o processo do servidor Flask ao fechar o aplicativo

if __name__ == '__main__':
    MainApp().run()
