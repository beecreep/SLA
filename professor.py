from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from db import db  # Removido o uso do connect_db
from flask_login import current_user, login_required
from models import User, Cronograma

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/professor')


#rota para o nome do professor
@login_required 
def professor(): 
    if current_user.role != 'Professor':
        return redirect(url_for('index'))
    return render_template('professor.html', nome=current_user.nome)

@professor_bp.route('/api/alunos', methods=['GET'])
@login_required
def get_alunos():
    if current_user.role != 'Professor':
        return jsonify({'erro': 'Acesso negado'}), 403

    alunos = User.query.filter_by(role='Aluno').with_entities(User.nome, User.turma).all()
    lista = [{'nome': aluno.nome, 'turma': aluno.turma} for aluno in alunos]
    
    return jsonify(alunos=lista)
