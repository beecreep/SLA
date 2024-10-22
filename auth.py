from flask import Blueprint, request, jsonify
from db import connect_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastrar', methods=['POST'])
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

@auth_bp.route('/login', methods=['POST'])
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
        role = user[6]  # Posição do 'role' na tabela
        if role == 'Aluno':
            return jsonify({'status': 'success', 'redirect_url': '/aluno'})
        elif role == 'Professor':
            return jsonify({'status': 'success', 'redirect_url': '/professor'})
    else:
        return jsonify({'status': 'Falha no login. Verifique suas credenciais.'})
