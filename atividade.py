from flask import  request, redirect, url_for, render_template, Blueprint,  send_file, session, jsonify
from flask_login import current_user, login_required
from db import db
from models import Atividade, Resposta, User
import mimetypes
import io

atividade_bp = Blueprint('atividade', __name__)

@atividade_bp.route('/prof-atv', methods=['POST'])
def professor_atv():
    # Verifica se o referer é a página 'professor.html'
    referer = request.headers.get("Referer")
    if current_user.role == 'Professor' and referer and '/professor' in referer:
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        arquivo = request.files['arquivo'].read() if 'arquivo' in request.files else None
        extensao = request.files['arquivo'].filename.split('.')[-1] if 'arquivo' in request.files else None

        nova_atividade = Atividade(titulo=titulo, descricao=descricao, arquivo=arquivo, extensao=extensao)
        db.session.add(nova_atividade)
        db.session.commit()

        return redirect(url_for('professor.professor'))  # Redireciona de volta para professor.html
    else:
        return "Ação não permitida", 403  # Código de status HTTP 403 para acesso proibido

@atividade_bp.route('/enviar_resposta', methods=['POST'])
def enviar_resposta():
    aluno_id = current_user.id
    atividade_id = request.form.get('atividade_id')
    resposta = request.form.get('resposta')
    arquivo_resposta = request.files['arquivo_resposta'].read() if 'arquivo_resposta' in request.files else None

    nova_resposta = Resposta(aluno_id=aluno_id, atividade_id=atividade_id, resposta=resposta, arquivo_resposta=arquivo_resposta)
    db.session.add(nova_resposta)
    db.session.commit()

    return redirect(f'/atividade/{aluno_id}')

# Função para buscar as atividades do banco de dados
def obter_atividades():
    atividades = Atividade.query.all()
    lista_atividades = [{
        'id': atividade.id,
        'titulo': atividade.titulo,
        'descricao': atividade.descricao,
        'data_envio': atividade.data_envio,
        'extensao': atividade.extensao
    } for atividade in atividades]
    return lista_atividades

@atividade_bp.route('/respostas', methods=['GET'])
@login_required
def obter_respostas():
    # Consulta para obter respostas com detalhes do aluno e da atividade
    respostas = db.session.query(
        User.nome.label("aluno"),
        Resposta.atividade_id,
        Resposta.resposta,
        Resposta.data_resposta
    ).join(User, User.id == Resposta.aluno_id).all()

    # Converte as respostas para um formato JSON
    respostas_data = [
        {
            "aluno": resposta.aluno,
            "atividade_id": resposta.atividade_id,
            "resposta": resposta.resposta,
            "data_resposta": resposta.data_resposta.strftime("%d/%m/%Y") if resposta.data_resposta else "N/A"
        }
        for resposta in respostas
    ]
    return jsonify(respostas_data)


# Rota para exibir as atividades
@atividade_bp.route('/atividade')
def atividade():
    atividades = obter_atividades()  # Obtém as atividades
    return render_template('atividade.html', atividades=atividades)


@atividade_bp.route('/download/<int:atividade_id>')
def download(atividade_id):
    atividade = Atividade.query.get(atividade_id)
    if atividade and atividade.arquivo:
        mime_type, _ = mimetypes.guess_type(f"arquivo.{atividade.extensao}")
        return send_file(io.BytesIO(atividade.arquivo), as_attachment=True,
                         download_name=f"arquivo_{atividade_id}.{atividade.extensao}", mimetype=mime_type)
    else:
        return "Arquivo não encontrado.", 404