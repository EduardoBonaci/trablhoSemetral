from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class Escolha(App):
    def build(self):

        layout = BoxLayout(orientation='vertical', size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})






        btn_cadastrar = Button(text='Cadastrar Livro', size_hint_y=None, height=30)
        btn_cadastrar.bind(on_press=self.on_login_pressed)

        btn_editar = Button(text='Editar Livro ', size_hint_y=None, height=30)
        btn_editar.bind(on_press=self.on_login_pressed)

        btn_login = Button(text='ver Livro ', size_hint_y=None, height=30)
        btn_login.bind(on_press=self.on_login_pressed)

        layout.add_widget(btn_login)
        layout.add_widget(btn_editar)
        layout.add_widget(btn_cadastrar)

        return layout



    def on_login_pressed(self, instance):
        # Adicione a lógica de login aqui
        print('Botão de login pressionado')

if __name__ == '__main__':
    Escolha().run()



