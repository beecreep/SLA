from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import connect_db
from flask_login import current_user
from db import db
from models import Atividade, Resposta

aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/aluno', methods=['GET', 'POST'])
def aluno():
    
    if current_user.role != 'Aluno':
        return redirect(url_for('index'))

    try:
        atividades = Atividade.query.all()
    except Exception as e:
        flash(f"Erro ao conectar ao banco de dados: {str(e)}")
        return render_template('aluno.html', atividades=[])

    if request.method == 'POST':
        atividade_id = request.form.get('atividade_id')
        resposta_texto = request.form.get('resposta')
        arquivo_resposta = request.files['arquivo_resposta'].read() if 'arquivo_resposta' in request.files else None

        # Verifica se todos os campos obrigatórios estão preenchidos
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
            db.session.add(nova_resposta)  # Adiciona a resposta ao banco de dados
            db.session.commit()
            flash("Resposta enviada com sucesso!")
        except Exception as e:
            db.session.rollback()  # Reverte a transação em caso de erro
            flash(f"Erro ao enviar resposta: {str(e)}")
        finally:
            return redirect(url_for('aluno.aluno'))

    return render_template('aluno.html', atividades=atividades, nome=current_user.nome)