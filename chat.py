
from db import connect_db
from flask import Blueprint, request, jsonify, session, render_template
from models import User, Mensagem
from db import db

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat():
    mensagens = db.session.query(User.username, Mensagem.mensagem).join(Mensagem.user).order_by(Mensagem.timestamp.asc()).all()
    return render_template('chat.html', mensagens=mensagens)

@chat_bp.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    if 'usuario_id' not in session:
        return jsonify({'status': 'Erro', 'message': 'Usuário não autenticado.'}), 401
    
    usuario_id = session['usuario_id']
    mensagem_texto = request.form['mensagem']

    nova_mensagem = Mensagem(usuario_id=usuario_id, mensagem=mensagem_texto)
    db.session.add(nova_mensagem)
    db.session.commit()

    return jsonify({'status': 'Mensagem enviada com sucesso!'})

@chat_bp.route('/carregar_mensagens', methods=['GET'])
def carregar_mensagens():
    mensagens = db.session.query(User.username, Mensagem.mensagem).join(Mensagem.user).order_by(Mensagem.timestamp.asc()).all()
    return jsonify(mensagens)


chat_bp = Blueprint('chat', __name__)

# Lista temporária de mensagens (idealmente, use um banco de dados)
mensagens = []
