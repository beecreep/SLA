
from db import db
from flask import Blueprint, request, jsonify, session, render_template, send_file
from models import User, Mensagem
from flask_login import current_user
import mimetypes
import io


chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat():
    mensagens = db.session.query(User.nome, Mensagem.mensagem, Mensagem.timestamp ).join(Mensagem.user).order_by(Mensagem.timestamp.asc()).all()
    return render_template('chat.html', mensagens=mensagens)

@chat_bp.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    if not current_user.is_authenticated:
      return jsonify({'status': 'Erro', 'message': 'Usuário não autenticado.'}), 401
   
    usuario_id = current_user.id 
    mensagem_texto = request.form.get('mensagem')
    arquivo = request.files.get('arquivo')

    # Criação da mensagem
    nova_mensagem = Mensagem(
        usuario_id=usuario_id,
        mensagem=mensagem_texto,
        arquivo=arquivo.read() if arquivo else None,
        extensao=arquivo.filename.split('.')[-1] if arquivo else None
    )

    db.session.add(nova_mensagem)
    db.session.commit()

     # Verificar se o número de mensagens excede 80
    total_mensagens = db.session.query(Mensagem).count()
    if total_mensagens > 80:
        # Apagar as 20 mensagens mais antigas
        mensagens_mais_antigas = db.session.query(Mensagem).order_by(Mensagem.timestamp.asc()).limit(20).all()
        for mensagem in mensagens_mais_antigas:
            db.session.delete(mensagem)
        db.session.commit()

    return render_template('chat.html',)

@chat_bp.route('/carregar_mensagens', methods=['GET'])
def carregar_mensagens():
    mensagens = db.session.query(
        User.nome, 
        Mensagem.mensagem, 
        Mensagem.id, 
        Mensagem.extensao, 
        Mensagem.timestamp
    ).join(Mensagem.user).order_by(Mensagem.timestamp.asc()).all()

    mensagens_formatadas = []
    for mensagem in mensagens:
        mensagem_dict = {
            'nome': mensagem.nome,  # Nome do usuário
            'mensagem': mensagem.mensagem,  # Texto da mensagem
            'arquivo_url': f"/chat/download/{mensagem.id}" if mensagem.extensao else None,  # URL do arquivo
            'extensao': mensagem.extensao,  # Extensão do arquivo
            'timestamp': mensagem.timestamp.strftime("%d/%m/%Y %H:%M"),  # Timestamp formatado
        }
        mensagens_formatadas.append(mensagem_dict)
        
    return jsonify(mensagens_formatadas)


@chat_bp.route('/download/<int:mensagem_id>')
def download_arquivo(mensagem_id):
    mensagem = Mensagem.query.get(mensagem_id)
    if mensagem and mensagem.arquivo:
        mime_type, _ = mimetypes.guess_type(f"arquivo.{mensagem.extensao}")
        return send_file(io.BytesIO(mensagem.arquivo), as_attachment=True,
                         download_name=f"arquivo_{mensagem_id}.{mensagem.extensao}", mimetype=mime_type)
    else:
        return "Arquivo não encontrado.", 404


