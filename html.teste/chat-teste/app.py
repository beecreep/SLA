from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('mensagens.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar a tabela de mensagens
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            role TEXT NOT NULL,
            mensagem TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    create_table()

# Rota para a página inicial com o formulário de login
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        role = request.form.get('role')
        
        # Verifique se ambos os campos foram preenchidos
        if nome and role:
            return redirect(url_for('chat', nome=nome, role=role))
        else:
            return "Por favor, preencha todos os campos corretamente.", 400

    return render_template('index.html')

# Rota para a página de chat
@app.route('/chat/<nome>/<role>', methods=['GET', 'POST'])
def chat(nome, role):
    conn = get_db_connection()
    if request.method == 'POST':
        mensagem = request.form.get('mensagem')
        if mensagem:
            conn.execute('INSERT INTO mensagens (nome, role, mensagem) VALUES (?, ?, ?)', (nome, role, mensagem))
            conn.commit()

    mensagens = conn.execute('SELECT * FROM mensagens').fetchall()
    conn.close()
    return render_template('chat.html', nome=nome, role=role, mensagens=mensagens)

if __name__ == '__main__':
    app.run(debug=True)
