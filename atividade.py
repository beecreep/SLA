from flask import  request, redirect, url_for, render_template, Blueprint,  send_file, session, jsonify
from flask_login import current_user, login_required
from db import db
from models import Atividade, Resposta, User, Cronograma
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
    extensao = request.files['arquivo_resposta'].filename.split('.')[-1] if 'arquivo_resposta' in request.files else None

    nova_resposta = Resposta(aluno_id=aluno_id, atividade_id=atividade_id, resposta=resposta, arquivo_resposta=arquivo_resposta, extensao=extensao)
    db.session.add(nova_resposta)
    db.session.commit()

    return render_template('atividade.html')

def obter_respostas():
    respostas = db.session.query(
        User.nome.label("aluno"), 
        Atividade.titulo.label("titulo_atividade"), 
        Resposta.resposta, 
        Resposta.data_resposta, 
        Resposta.id, 
        Resposta.arquivo_resposta
    ).join(Resposta.user).join(Resposta.atividade).all()

    lista_respostas = [
        {
            "aluno": resposta.aluno,
            "titulo_atividade": resposta.titulo_atividade,
            "resposta": resposta.resposta,
            "data_resposta": resposta.data_resposta.strftime("%d/%m/%Y") if resposta.data_resposta else "",
            "arquivo_resposta_id": resposta.id if resposta.arquivo_resposta else None
        }
        for resposta in respostas
    ]
    return lista_respostas

@atividade_bp.route('/respostas')
def respostas():
    lista_respostas = obter_respostas()  # Obtém as respostas formatadas
    return render_template('respostas.html', respostas=lista_respostas)


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

@atividade_bp.route('/download_resposta/<int:resposta_id>')
def download_resposta(resposta_id):
   # Obtenha a resposta pelo ID
    resposta = Resposta.query.get(resposta_id)
    
    # Verifique se a resposta existe e possui um arquivo
    if resposta and resposta.arquivo_resposta:
        # Defina o tipo MIME com base na extensão do arquivo
        mime_type, _ = mimetypes.guess_type(f"arquivo_resposta.{resposta.extensao}")
        
        # Envie o arquivo como um download
        return send_file(io.BytesIO(resposta.arquivo_resposta), as_attachment=True,
                         download_name=f"resposta_{resposta_id}.{resposta.extensao}", mimetype=mime_type)
    else:
        return "Arquivo de resposta não encontrado.", 404