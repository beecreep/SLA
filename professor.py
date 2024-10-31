from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from db import connect_db
from flask_login import current_user

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/professor')
def professor(): 
    if current_user.role != 'professor':
        return redirect(url_for('/'))
      # Redireciona se não estiver autenticado como professor

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        arquivo = request.files['arquivo'].read() if 'arquivo' in request.files else None

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO atividades (titulo, descricao, arquivo) VALUES (?, ?, ?)',
                       (titulo, descricao, arquivo))
        conn.commit()
        conn.close()

        return "Atividade enviada com sucesso!"
    return render_template('professor.html',  nome=current_user.nome )

@professor_bp.route('/api/alunos', methods=['GET'])
def get_alunos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, turma FROM usuarios WHERE role = 'Aluno'")
    alunos = [{'nome': row[0], 'turma': row[1]} for row in cursor.fetchall()]
    conn.close()

    return jsonify(alunos=alunos)
