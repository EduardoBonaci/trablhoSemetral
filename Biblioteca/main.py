import subprocess
from threading import Thread

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from tela_cadastro_livros import CadastroLivroScreen
from tela_cadastro_usuario import CadastroUsuarioScreen
from tela_login import LoginScreen
from tela_usuarios import ListaUsuariosScreen

class MyApp(App):
    def build(self):
        """Construção da aplicação Kivy."""
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CadastroUsuarioScreen(name='tela_cadastro_usuario'))
        sm.add_widget(ListaUsuariosScreen(name='lista'))
        sm.add_widget(CadastroLivroScreen(name='cadastro_livro'))
        return sm

    def on_start(self):
        """Inicia o servidor Flask em uma thread separada ao iniciar a aplicação."""
        Thread(target=self.iniciar_servidor_flask).start()

    def iniciar_servidor_flask(self):
        """Inicia o servidor Flask utilizando subprocess.Popen."""
        comando = ['python', 'backend.py', 'run', '--host=0.0.0.0']
        try:
            subprocess.Popen(comando)
        except subprocess.SubprocessError as e:
            print(f'Erro ao iniciar o servidor Flask: {e}')
        except Exception as e:
            print(f'Ocorreu um erro inesperado ao iniciar o servidor Flask: {e}')

if __name__ == '__main__':
    MyApp().run()
