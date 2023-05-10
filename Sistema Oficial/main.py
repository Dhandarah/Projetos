from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, session
import mysql.connector
from hashlib import sha256
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Função para cadastrar motorista
def cadastrar_motorista(nome, sobrenome, cpf, cnh, modelo_veiculo, placa, usuario, senha):
    # Conectar ao banco de dados MySQL
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transporte"
    )

    cursor = cnx.cursor()

    # Hash da senha fornecida
    senha_hash = sha256(senha.encode()).hexdigest()

    # Inserir dados do motorista no banco de dados
    query = """
    INSERT INTO motoristas (nome, sobrenome, cpf, cnh, modelo_veiculo, placa, usuario, senha, salt)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nome, sobrenome, cpf, cnh, modelo_veiculo, placa, usuario, senha, senha_hash))

    # Commit das alterações e fechar conexões
    cnx.commit()
    cursor.close()
    cnx.close()


# Função para atualizar o status do motorista
def atualizar_status_motorista(usuario, status):
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transporte"
    )

    cursor = cnx.cursor()

    query = "UPDATE motoristas SET status = %s WHERE usuario = %s"
    cursor.execute(query, (status, usuario))

    cnx.commit()
    cursor.close()
    cnx.close()


@app.route('/status_motorista', methods=['POST'])
def status_motorista():
    usuario = request.form['usuario']
    status = request.form['status']
    
    atualizar_status_motorista(usuario, status)
    return "Status atualizado"


@app.route('/')
def index():
    motoristas = listar_motoristas()
    return render_template('index.html', motoristas=motoristas)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        cpf = request.form['cpf']
        cnh = request.form['cnh']
        modelo_veiculo = request.form['modelo_veiculo']
        placa = request.form['placa']
        usuario = request.form['usuario']
        senha = request.form['senha']

        cadastrar_motorista(nome, sobrenome, cpf, cnh, modelo_veiculo, placa, usuario, senha)
        return redirect('/')

    return render_template('cadastro.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash da senha fornecida
        password_hash = sha256(password.encode()).hexdigest()

        # Conectar ao banco de dados MySQL
        cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transporte"
        )

        cursor = cnx.cursor()

        # Verificar se o usuário e a senha estão corretos
        query = """
        SELECT COUNT(*)
        FROM motoristas
        WHERE usuario = %s AND senha = %s
        """

        cursor.execute(query, (username, password_hash))
        result = cursor.fetchone()

        # Se o usuário e a senha estiverem corretos, redirecionar para a página do usuário
        if result[0] == 1:
            session['username'] = username
            return redirect(url_for('user_page'))
        else:
            flash('Usuário ou senha inválidos. Tente novamente.')

        # Fechar conexões
        cursor.close()
        cnx.close()

    return render_template('login.html', error=error)


def obter_motorista(usuario):
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transporte"
    )

    cursor = cnx.cursor()

    query = """
    SELECT nome, sobrenome, cpf, cnh, modelo_veiculo, placa, status
    FROM motoristas
    WHERE usuario = %s
    """

    cursor.execute(query, (usuario,))
    result = cursor.fetchone()

    cursor.close()
    cnx.close()

    if result:
        motorista = {
            'nome': result[0],
            'sobrenome': result[1],
            'cpf': result[2],
            'cnh': result[3],
            'modelo_veiculo': result[4],
            'placa': result[5],
            'status': result[6]
        }
        return motorista
    else:
        return None
    
def listar_motoristas():
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transporte"
    )

    cursor = cnx.cursor()

    query = "SELECT nome, sobrenome, modelo_veiculo, placa, status FROM motoristas"
    cursor.execute(query)

    motoristas = cursor.fetchall()
    cursor.close()
    cnx.close()

    return motoristas



@app.route('/usuario')
def user_page():
    motorista = obter_motorista(session['username'])
    print("Motorista:", motorista)  # Adicione esta linha
    return render_template('usuario.html', motorista=motorista)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)