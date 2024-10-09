from flask import Flask, redirect, render_template, request, jsonify, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect('usuarios.db')
    print("Conexão com banco de dados estabelecida")
    return conn

# Função para criar a tabela de usuários
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL,
                        senha TEXT NOT NULL,
                        turma TEXT,
                        numero TEXT,
                        role TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        filename TEXT NOT NULL,
                        filedata BLOB NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

# Cria a tabela ao iniciar o servidor
create_table()

# Rota para servir o arquivo HTML (cadastro.html)
@app.route('/')
def index():
    return render_template('cadastro.html')

# Rota para cadastrar um novo usuário
@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    
    nome = data['nome']
    email = data['email']
    senha = data['senha']
    turma = data.get('turma', '')
    numero = data.get('numero', '')
    role = data['role']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO usuarios (nome, email, senha, turma, numero, role)
                      VALUES (?, ?, ?, ?, ?, ?)''', (nome, email, senha, turma, numero, role))
    conn.commit()
    conn.close()

    return jsonify({'status': 'Usuário cadastrado com sucesso!'})

# Rota para fazer login
@app.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    email = data['email']
    senha = data['senha']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email=? AND senha=?', (email, senha))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Verifica o papel do usuário (Aluno ou Professor)
        role = user[6]  # A posição do 'role' na tabela, provavelmente a 6ª coluna
        if role == 'Aluno':
            return jsonify({'status': 'success', 'redirect_url': '/aluno'})
        elif role == 'Professor':
            return jsonify({'status': 'success', 'redirect_url': '/professor'})
    else:
        return jsonify({'status': 'Falha no login. Verifique suas credenciais.'})
    
    if user:
        # Verifica o papel do usuário (Aluno ou Professor)
        role = user[6]  # A posição do 'role' na tabela, provavelmente a 6ª coluna
        if role == 'Aluno':
            return redirect(url_for('aluno'))
        elif role == 'Professor':
            return redirect(url_for('professor'))
    else:
        return jsonify({'status': 'Falha no login. Verifique suas credenciais.'})


# Rota para a página de aluno
@app.route('/aluno')
def aluno():
    return render_template('aluno.html')

# Rota para a página de professor
@app.route('/professor')
def professor():
    return render_template('professor.html')

if __name__ == '__main__':
    app.run(debug=True)
