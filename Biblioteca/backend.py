from flask import Flask, request, jsonify, session
import cx_Oracle

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Dados da conexão Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='xe')
conn = cx_Oracle.connect(user='hr2', password='1510', dsn=dsn_tns)

@app.route('/login', methods=['POST'])
def login():
    try:
        connection = cx_Oracle.connect(user='hr2', password='1010', dsn=dsn_tns)
        cursor = connection.cursor()

        nome_usuario = request.form.get('nome_usuario')
        senha = request.form.get('senha')

        if not nome_usuario or not senha:
            return 'Nome de usuário e senha são obrigatórios!', 400

        cursor.execute("SELECT is_admin FROM usuarios WHERE nome = :nome AND senha = :senha",
                       {'nome': nome_usuario, 'senha': senha})
        result = cursor.fetchone()

        if result is None:
            return 'Nome de usuário ou senha incorretos!', 401

        is_admin = result[0]
        session['is_admin'] = is_admin

        return jsonify({'message': 'Login bem-sucedido!', 'is_admin': is_admin}), 200
    except cx_Oracle.DatabaseError as error:
        return f'Erro ao verificar credenciais: {error}', 500
    finally:
        cursor.close()
        connection.close()

@app.route('/listar_usuarios', methods=['GET'])
def listar_usuarios():
    try:
        connection = cx_Oracle.connect(user='hr2', password='1010', dsn=dsn_tns)
        cursor = connection.cursor()

        cursor.execute("SELECT nome, senha, is_admin FROM usuarios")
        users = [{'nome': row[0], 'senha': row[1], 'admin': row[2]} for row in cursor.fetchall()]

        return jsonify(users), 200
    except cx_Oracle.DatabaseError as error:
        return f'Erro ao listar usuários: {error}', 500
    finally:
        cursor.close()
        connection.close()

@app.route('/verificar_cadastro', methods=['POST'])
def verificar_cadastro():
    nome_usuario = request.form['nome_usuario']
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nome_usuario = :nome_usuario", {'nome_usuario': nome_usuario})
    result = cursor.fetchone()
    existe = result[0] > 0
    cursor.close()
    return jsonify({'existe': existe})

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome_usuario = request.form['nome_usuario']
    senha = request.form['senha']
    is_admin = int(request.form['is_admin'])
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome_usuario, senha, is_admin) VALUES (:nome_usuario, :senha, :is_admin)",
                       {'nome_usuario': nome_usuario, 'senha': senha, 'is_admin': is_admin})
        conn.commit()
        return jsonify({'status': 'success'})
    except cx_Oracle.DatabaseError as e:
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        cursor.close()

@app.route('/excluir_usuario', methods=['POST'])
def excluir_usuario():
    try:
        connection = cx_Oracle.connect(user='hr2', password='1010', dsn=dsn_tns)
        cursor = connection.cursor()

        nome_usuario = request.form.get('nome_usuario')

        if not nome_usuario:
            return 'Nome de usuário é obrigatório!', 400

        cursor.execute("DELETE FROM usuarios WHERE nome = :nome", {'nome': nome_usuario})
        connection.commit()

        return jsonify({'message': 'Usuário excluído com sucesso!'}), 200
    except cx_Oracle.DatabaseError as error:
        return f'Erro ao excluir usuário: {error}', 500
    finally:
        cursor.close()
        connection.close()

@app.route('/cadastrar_livro', methods=['POST'])
def cadastrar_livro():
    try:
        connection = cx_Oracle.connect(user='hr2', password='1010', dsn=dsn_tns)
        cursor = connection.cursor()

        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        ano = request.form.get('ano')
        editora = request.form.get('editora')

        if not titulo or not autor or not ano or not editora:
            return 'Todos os campos são obrigatórios!', 400

        cursor.execute("SELECT NVL(MAX(id), 0) FROM livros")
        max_id = cursor.fetchone()[0]
        new_id = max_id + 1

        cursor.execute("INSERT INTO livros (id, titulo, autor, ano_publicacao, editora) VALUES (:id, :titulo, :autor, :ano, :editora)",
                       {'id': new_id, 'titulo': titulo, 'autor': autor, 'ano': ano, 'editora': editora})
        connection.commit()

        return jsonify({'message': 'Livro cadastrado com sucesso!'}), 200
    except cx_Oracle.DatabaseError as error:
        return f'Erro ao cadastrar livro: {error}', 500
    finally:
        cursor.close()
        connection.close()

@app.route('/listar_livros', methods=['GET'])
def listar_livros():
    try:
        connection = cx_Oracle.connect(user='hr2', password='1010', dsn=dsn_tns)
        cursor = connection.cursor()

        cursor.execute("SELECT id, titulo, autor, ano_publicacao, editora FROM livros")
        livros = [{'id': livro[0], 'titulo': livro[1], 'autor': livro[2], 'ano': livro[3], 'editora': livro[4]} for livro in cursor.fetchall()]

        return jsonify(livros), 200
    except cx_Oracle.DatabaseError as error:
        return f'Erro ao listar livros: {error}', 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
