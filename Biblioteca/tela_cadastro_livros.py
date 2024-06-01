import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

class CadastroLivroScreen(Screen):
    def __init__(self, **kwargs):
        super(CadastroLivroScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})

        lbl_titulo = Label(text='Título')
        self.txt_titulo = TextInput(multiline=False, size_hint_y=None, height=30)
        layout.add_widget(lbl_titulo)
        layout.add_widget(self.txt_titulo)

        lbl_autor = Label(text='Autor')
        self.txt_autor = TextInput(multiline=False, size_hint_y=None, height=30)
        layout.add_widget(lbl_autor)
        layout.add_widget(self.txt_autor)

        lbl_ano_publicacao = Label(text='Ano de Publicação')
        self.txt_ano_publicacao = TextInput(multiline=False, size_hint_y=None, height=30)
        layout.add_widget(lbl_ano_publicacao)
        layout.add_widget(self.txt_ano_publicacao)

        self.lbl_aviso = Label(text='', color=(1, 0, 0, 1))  # Label para exibir aviso em vermelho
        layout.add_widget(self.lbl_aviso)

        btn_cadastrar = Button(text='Cadastrar Livro', size_hint_y=None, height=30)
        btn_cadastrar.bind(on_press=self.cadastrar_livro)
        layout.add_widget(btn_cadastrar)

        self.add_widget(layout)

    def cadastrar_livro(self, instance):
        titulo = self.txt_titulo.text
        autor = self.txt_autor.text
        ano_publicacao = self.txt_ano_publicacao.text

        if not titulo or not autor or not ano_publicacao:
            self.lbl_aviso.text = 'Todos os campos são obrigatórios!'
        else:
            try:
                ano_publicacao = int(ano_publicacao)  # Convertendo o ano para inteiro
                data = {
                    'titulo': titulo,
                    'autor': autor,
                    'ano_publicacao': ano_publicacao
                }
                response = requests.post('http://localhost:5000/cadastrar_livro', json=data)
                if response.status_code == 200:
                    self.mostrar_popup('Sucesso', 'Livro cadastrado com sucesso!')
                    self.limpar_campos()
                else:
                    self.lbl_aviso.text = 'Erro ao cadastrar livro: ' + response.text
            except ValueError:
                self.lbl_aviso.text = 'O ano de publicação deve ser um número válido!'
            except requests.RequestException as e:
                self.lbl_aviso.text = 'Erro de conexão: ' + str(e)

    def limpar_campos(self):
        self.txt_titulo.text = ''
        self.txt_autor.text = ''
        self.txt_ano_publicacao.text = ''
        self.lbl_aviso.text = ''

    def mostrar_popup(self, titulo, mensagem):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=mensagem)
        fechar_button = Button(text='Fechar', size_hint=(None, None), size=(100, 50))
        layout.add_widget(popup_label)
        layout.add_widget(fechar_button)
        popup = Popup(title=titulo, content=layout, size_hint=(None, None), size=(400, 200))
        fechar_button.bind(on_press=popup.dismiss)
        popup.open()
