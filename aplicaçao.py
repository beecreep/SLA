from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'seupai123@sherekbr12'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota para carregar a página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('home_page.html')  # Renderiza o arquivo cadastro.html

# Rota para registro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome =request.form.get('nome')
    email =request.form.get('email')
    senha =request.form.get('senha')
    turma =request.form.get('turma')
    numero =request.form.get('numero')
    role =request.form.get('role')
    
    # Verificação de senha
    hashed_password = generate_password_hash(senha)

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (nome, email, senha, turma, numero, role) VALUES (?, ?, ?, ?, ?, ?)',
                     (nome, email, hashed_password, turma, numero, role))
        conn.commit()

        # Adiciona o nome do aluno à lista de chamada
        if role.lower() == 'aluno':  # Só adiciona se for aluno
            adicionar_a_lista_chamada(nome)

        return jsonify({"status": "Cadastro bem-sucedido"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "Erro: Email já cadastrado"}), 400
    finally:
        conn.close()

# Outras rotas (login, upload, etc.) permanecem iguais...

if __name__ == '__main__':
    app.run(debug=True)
