from flask import Flask, request, render_template
import cx_Oracle

app = Flask(__name__)

# Configuração do banco de dados Oracle
dsn_tns = cx_Oracle.makedsn('EDU', '1521', service_name='xe')
connection = cx_Oracle.connect(user='hr2', password='1010', dsn=dsn_tns)
cursor = connection.cursor()




@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario')
        senha = request.form.get('senha')

        if not nome_usuario or not senha:
            return 'Nome de usuário e senha são obrigatórios!', 400

        try:
            cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (:nome, :senha)",
                           {'nome': nome_usuario, 'senha': senha})
            connection.commit()
            return 'Usuário cadastrado com sucesso!', 200
        except cx_Oracle.DatabaseError as error:
            error_msg = f'Erro ao cadastrar usuário: {error}'
            return error_msg, 500






if __name__ == '__main__':
    app.run(debug=True)
