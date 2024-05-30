import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class CadastroLivroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(layout)

        self.label_titulo = Label(text='Título')
        self.input_titulo = TextInput()

        self.label_autor = Label(text='Autor')
        self.input_autor = TextInput()

        self.label_ano = Label(text='Ano de Publicação')
        self.input_ano = TextInput()

        self.label_editora = Label(text='Editora')
        self.input_editora = TextInput()

        self.btn_cadastrar = Button(text='Cadastrar Livro')
        self.btn_cadastrar.bind(on_press=self.cadastrar_livro)

        layout.add_widget(self.label_titulo)
        layout.add_widget(self.input_titulo)
        layout.add_widget(self.label_autor)
        layout.add_widget(self.input_autor)
        layout.add_widget(self.label_ano)
        layout.add_widget(self.input_ano)
        layout.add_widget(self.label_editora)
        layout.add_widget(self.btn_cadastrar)

    def cadastrar_livro(self, instance):
        titulo = self.input_titulo.text
        autor = self.input_autor.text
        ano = self.input_ano.text
        editora = self.input_editora.text

        response = requests.post('http://localhost:5000/cadastrar_livro',
                                 data={'titulo': titulo, 'autor': autor, 'ano': ano, 'editora': editora})
        if response.status_code == 200:
            popup = Popup(title='Sucesso',
                          content=Label(text='Livro cadastrado com sucesso!'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            popup = Popup(title='Erro',
                          content=Label(text='Erro ao cadastrar livro!'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
