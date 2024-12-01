from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import Cronograma
from db import db
from flask_login import login_required, current_user

cronogramas_bp = Blueprint('cronogramas', __name__)

@cronogramas_bp.route('/cronogramas_prof', methods=['GET', 'POST'])
def cronogramas_prof():

    # Lista de turmas disponíveis
    turmas = ["Eletronica", "Segurança do trabalho", "Administração", "Eventos"]
    # Horários fixos
    horarios = [
    "07:00 - 07:50",
    "07:50 - 08:40",
    "08:40 - 09:30",
    "10:00 - 10:50",
    "10:50 - 11:30",
    "11:30 - 12:20"
]
    
    cronogramas = Cronograma.query.order_by(Cronograma.turma, Cronograma.dia_semana, Cronograma.horario).all()
    turmas = {cronograma.turma for cronograma in cronogramas}

    return render_template('cronogramas-prof.html', horarios=horarios,
        cronogramas=cronogramas,
        turmas=sorted(turmas)) 

@cronogramas_bp.route('/cronogramas_aluno')
@login_required
def cronogramas_aluno():

    turma_aluno = current_user.turma

    if not turma_aluno:
        return render_template(
            'cronogramas-aluno.html',
            cronogramas={},
            mensagem="Nenhuma turma associada ao usuário."
        )

    # Busca os cronogramas correspondentes à turma do aluno
    cronogramas_db = Cronograma.query.filter_by(turma=turma_aluno).order_by(
        Cronograma.dia_semana, Cronograma.horario
    ).all()

    cronogramas_organizados = {
        'segunda': [],
        'terca': [],
        'quarta': [],
        'quinta': [],
        'sexta': []
    }

    # Mapeamento entre dias do banco de dados e chaves do dicionário
    dias_map = {
        'Segunda': 'segunda',
        'Terça': 'terca',
        'Quarta': 'quarta',
        'Quinta': 'quinta',
        'Sexta': 'sexta'
    }

    for cronograma in cronogramas_db:
        dia_key = dias_map.get(cronograma.dia_semana)
        if dia_key:
            cronogramas_organizados[dia_key].append({
                'horario': cronograma.horario,
                'aula': cronograma.aula,
                'intervalo': cronograma.horario == "09:30 - 09:50"  # Verifica se é horário de intervalo
            })

    return render_template('cronogramas-aluno.html',  cronogramas=cronogramas_organizados,  mensagem=None)
 
@cronogramas_bp.route('/cronogramas', methods=['GET', 'POST'])
@login_required
def gerenciar_cronograma():
    if request.method == 'POST':
        turma = request.form.get('turma')
        dia_semana = request.form.get('dia_semana')
        horario = request.form.get('horario')
        aula = request.form.get('aula')
        professor = request.form.get('professor')

        if not dia_semana or not horario or not aula or not professor:
            flash("Todos os campos devem ser preenchidos.")
            return redirect(url_for('cronogramas.gerenciar_cronogramas'))

        usuario_id = current_user.id

        # Atualizar ou criar o cronograma
        cronograma_existente = Cronograma.query.filter_by(
             usuario_id=usuario_id,turma=turma, dia_semana=dia_semana, horario=horario).first()
        if cronograma_existente:
            cronograma_existente.aula = aula
            cronograma_existente.professor = professor
        else:
            novo_cronograma = Cronograma(
                usuario_id=usuario_id,
                turma=turma,
                dia_semana=dia_semana,
                horario=horario,
                aula=aula,
                professor=professor
            )
            db.session.add(novo_cronograma)

        db.session.commit()
        flash("Cronograma atualizado com sucesso!")
        return redirect(url_for('cronogramas.cronogramas_prof'))
    
    # Busca os cronogramas existentes para exibição
    cronogramas = Cronograma.query.filter_by(usuario_id=current_user.id).order_by(
        Cronograma.dia_semana, Cronograma.horario
    ).all()
    horarios = [
        "07:00 - 07:50", "07:50 - 08:40", "08:40 - 09:30",
        "09:30 - 09:50 (Intervalo)", "09:50 - 10:40", "10:40 - 11:30",
        "11:30 - 12:20"
    ]

    # Obter cronogramas para a turma
    cronogramas = Cronograma.query.filter_by(turma=turma).all()
    return render_template('cronograma.html', turma=turma, horarios=horarios, cronogramas=cronogramas)
