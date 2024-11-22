
from db import connect_db
from flask import Blueprint, request, jsonify, session, render_template
from models import User, Mensagem
from db import db
from flask_login import current_user

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat():
    mensagens = db.session.query(User.nome, Mensagem.mensagem).join(Mensagem.user).order_by(Mensagem.timestamp.asc()).all()
    return render_template('chat.html', mensagens=mensagens)

@chat_bp.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    if not current_user.is_authenticated:
      return jsonify({'status': 'Erro', 'message': 'Usuário não autenticado.'}), 401
    
    data = request.get_json()
    usuario_id = current_user.id 
    mensagem_texto = data['mensagem']

    nova_mensagem = Mensagem(usuario_id=usuario_id, mensagem=mensagem_texto)
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

    return jsonify({'status': 'Mensagem enviada com sucesso!'})

@chat_bp.route('/carregar_mensagens', methods=['GET'])
def carregar_mensagens():
    mensagens = db.session.query(User.nome, Mensagem.mensagem).join(Mensagem.user).order_by(Mensagem.timestamp.asc()).all()

    mensagens_data = [
        {
            'username': mensagem[0],
            'text': mensagem[1],
            'timestamp': mensagem[2].strftime("%d/%m/%Y %H:%M")
        }
        for mensagem in mensagens
    ]
    return jsonify(mensagens_data)

