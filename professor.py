from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from db import db, connect_db  # Importando diretamente de db.py
from flask_login import current_user, login_required
from models import User, Atividade

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/professor')
def professor(): 
    
    if current_user.role != 'Professor':
        return redirect(url_for('index'))
    
      # Redireciona se não estiver autenticado como professor
    return render_template('professor.html',  nome=current_user.nome )

@professor_bp.route('/api/alunos', methods=['GET'])
def get_alunos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, turma FROM usuarios WHERE role = 'Aluno'")
    alunos = [{'nome': row[0], 'turma': row[1]} for row in cursor.fetchall()]
    conn.close()

    return jsonify(alunos=alunos)
