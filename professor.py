from flask import Blueprint, request, render_template, redirect, url_for
from db import connect_db

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/professor', methods=['GET', 'POST'])
def professor():
    conn = connect_db()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        arquivo = request.files['arquivo'].read() if 'arquivo' in request.files else None

        conn.execute('INSERT INTO atividades (titulo, descricao, arquivo) VALUES (?, ?, ?)',
                     (titulo, descricao, arquivo))
        conn.commit()

    atividades = conn.execute('SELECT * FROM atividades').fetchall()
    respostas = conn.execute('''SELECT r.id, u.nome AS aluno_nome, a.titulo AS atividade_titulo, r.resposta, r.data_resposta
                                FROM respostas r
                                JOIN usuarios u ON r.aluno_id = u.id
                                JOIN atividades a ON r.atividade_id = a.id''').fetchall()
    conn.close()

    return render_template('professor.html', atividades=atividades, respostas=respostas)
