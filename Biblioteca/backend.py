from flask import Flask, request, jsonify
import cx_Oracle

app = Flask(__name__)

# Função para conectar ao banco de dados Oracle
def get_db_connection():
    try:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='xe')
        connection = cx_Oracle.connect(user='hr2', password='1010', dsn=dsn_tns)
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Erro ao conectar ao banco de dados Oracle:", error)
        return None

# Estabelecendo conexão com o Banco de Dados Oracle
connection = get_db_connection()

@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    if connection is None:
        return jsonify({'error': 'Falha na conexão com o banco de dados'}), 500

    try:
        data = request.json
        nome = data['nome']
        senha = data['senha']
        admin = int(data.get('admin', 0))  # Convertendo para inteiro e tratando caso 'admin' não esteja presente

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO usuarios (nome, senha, admin) VALUES (:1, :2, :3)", (nome, senha, admin))
            connection.commit()

        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 200

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'error': str(error)}), 500
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    if connection is None:
        return jsonify({'error': 'Falha na conexão com o banco de dados'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome, admin FROM usuarios")
            usuarios = [{'nome': row[0], 'admin': row[1]} for row in cursor.fetchall()]

        return jsonify(usuarios), 200

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'error': str(error)}), 500

@app.route('/login', methods=['POST'])
def login():
    if connection is None:
        return jsonify({'error': 'Falha na conexão com o banco de dados'}), 500

    try:
        data = request.json
        nome = data['nome']
        senha = data['senha']

        with connection.cursor() as cursor:
            cursor.execute("SELECT senha, admin FROM usuarios WHERE nome = :1", (nome,))
            result = cursor.fetchone()

        if result:
            db_senha, admin = result
            if db_senha == senha:
                return jsonify({'admin': admin, 'status': 'success'}), 200
            else:
                return jsonify({'error': 'Senha incorreta!', 'status': 'failure'}), 401
        else:
            return jsonify({'error': 'Usuário não encontrado!', 'status': 'failure'}), 404

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'error': str(error), 'status': 'failure'}), 500
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}', 'status': 'failure'}), 400


@app.route('/cadastrar_livro', methods=['POST'])
def cadastrar_livro():
    if connection is None:
        return jsonify({'error': 'Falha na conexão com o banco de dados'}), 500

    try:
        data = request.json
        titulo = data['titulo']
        autor = data['autor']
        ano_publicacao = data['ano_publicacao']

        if not titulo or not autor or not ano_publicacao:
            return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO livros (titulo, autor, ano_publicacao) 
                VALUES (:1, :2, :3)
            """, (titulo, autor, ano_publicacao))
            connection.commit()

        return jsonify({'message': 'Livro cadastrado com sucesso!'}), 200

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'error': str(error)}), 500

@app.route('/listar_livros', methods=['GET'])
def listar_livros():
    if connection is None:
        return jsonify({'error': 'Falha na conexão com o banco de dados'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT titulo, autor, ano_publicacao FROM livros")
            livros = [{'titulo': row[0], 'autor': row[1], 'ano_publicacao': row[2]} for row in cursor.fetchall()]

        return jsonify({'livros': livros}), 200

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'error': str(error)}), 500
@app.route('/usuarios/<nome>', methods=['GET'])
def verificar_usuario(nome):
    if connection is None:
        return jsonify({'error': 'Falha na conexão com o banco de dados'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome FROM usuarios WHERE nome = :1", (nome,))
            result = cursor.fetchone()

        if result:
            return jsonify({'message': 'Usuário já existe!'}), 200
        else:
            return jsonify({'message': 'Usuário disponível!'}), 404

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'error': str(error)}), 500


if __name__ == '__main__':
    app.run(debug=True)
