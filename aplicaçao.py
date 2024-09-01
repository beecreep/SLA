from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para adicionar aluno ao arquivo JSON de lista de chamada
def adicionar_a_lista_chamada(nome):
    lista_chamada_path = 'listachamada.json'
    
    # Verifica se o arquivo existe, caso contrário, cria um novo
    if not os.path.exists(lista_chamada_path):
        with open(lista_chamada_path, 'w') as f:
            json.dump({"alunos": []}, f)
    
    # Lê o conteúdo atual da lista
    with open(lista_chamada_path, 'r') as f:
        lista_chamada = json.load(f)
    
    # Adiciona o novo aluno à lista
    lista_chamada['alunos'].append(nome)
    
    # Salva a lista atualizada
    with open(lista_chamada_path, 'w') as f:
        json.dump(lista_chamada, f, indent=4)

# Rota para registro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.json.get('nome')
    email = request.json.get('email')
    senha = request.json.get('senha')
    turma = request.json.get('turma')
    numero = request.json.get('numero')
    role = request.json.get('role')
    
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
