from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from db import db
from models import Atividade, Resposta, Cronograma

aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/aluno', methods=['GET', 'POST'])
@login_required
def aluno():
    if current_user.role != 'Aluno':
        return redirect(url_for('index'))

    atividades = Atividade.query.all()

    if request.method == 'POST':
        atividade_id = request.form.get('atividade_id')
        resposta_texto = request.form.get('resposta')
        arquivo = request.files.get('arquivo_resposta')
        arquivo_resposta = arquivo.read() if arquivo else None

        if not atividade_id or not resposta_texto:
            flash("Por favor, preencha todos os campos obrigatórios.")
            return redirect(url_for('aluno.aluno'))

        nova_resposta = Resposta(
            aluno_id=current_user.id,
            atividade_id=atividade_id,
            resposta=resposta_texto,
            arquivo_resposta=arquivo_resposta
        )

        try:
            db.session.add(nova_resposta)
            db.session.commit()
            flash("Resposta enviada com sucesso!")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao enviar resposta: {str(e)}")
        finally:
            return redirect(url_for('aluno.aluno'))

    cronogramas = Cronograma.query.all()
    return render_template('aluno.html', atividades=atividades, nome=current_user.nome, cronogramas=cronogramas)

@aluno_bp.route('/cronogramas', methods=['GET'])
@login_required
def obter_cronogramas():
    return redirect(url_for('aluno.aluno'))  # Redireciona para rota principal que já mostra cronogramas
