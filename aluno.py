from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import connect_db

aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/aluno', methods=['GET', 'POST'])
def aluno():
    try:
        conn = connect_db()
        atividades = conn.execute('SELECT * FROM atividades').fetchall()
    except Exception as e:
        flash("Erro ao conectar ao banco de dados: {}".format(str(e)))
        return render_template('aluno.html', atividades=[])

    if request.method == 'POST':
        aluno_id = request.form.get('aluno_id')
        atividade_id = request.form.get('atividade_id')
        resposta = request.form.get('resposta')
        arquivo_resposta = request.files['arquivo_resposta'].read() if 'arquivo_resposta' in request.files else None

        # Verificar se todos os campos necessários estão preenchidos
        if not aluno_id or not atividade_id or not resposta:
            flash("Por favor, preencha todos os campos obrigatórios.")
            return redirect(url_for('aluno.aluno'))

        try:
            conn.execute('INSERT INTO respostas (aluno_id, atividade_id, resposta, arquivo_resposta) VALUES (?, ?, ?, ?) ',
                         (aluno_id, atividade_id, resposta, arquivo_resposta))
            conn.commit()
        except Exception as e:
            flash("Erro ao inserir resposta: {}".format(str(e)))
            return redirect(url_for('aluno.aluno'))
        finally:
            conn.close()

        return redirect(url_for('aluno.aluno'))

    return render_template('aluno.html', atividades=atividades)
