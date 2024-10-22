from flask import Blueprint, request, jsonify, render_template
from db import connect_db

chat_bp = Blueprint('chat', __name__)

# Lista temporária de mensagens (idealmente, use um banco de dados)
mensagens = []

# Rota para exibir a página do chat
@chat_bp.route('/chat')
def chat():
    return render_template('chat.html')

# Rota para enviar uma mensagem no chat
@chat_bp.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    data = request.get_json()
    usuario_id = data['usuario_id']
    mensagem = data['mensagem']

    # Conecte-se ao banco de dados para recuperar o nome do usuário
    conn = connect_db()
    cursor = conn.cursor()
    
    # Buscando o nome do usuário
    cursor.execute('SELECT nome FROM usuarios WHERE id=?', (usuario_id,))
    result = cursor.fetchone()
    
    # Verifica se o usuário foi encontrado
    if result is None:
        return jsonify({'status': 'Erro', 'message': 'Usuário não encontrado.'}), 404

    nome_usuario = result[0]  # Nome do usuário encontrado
    conn.close()

    # Formata a mensagem com o nome do usuário
    mensagem_formatada = {'usuario': nome_usuario, 'mensagem': mensagem}
    mensagens.append(mensagem_formatada)

    return jsonify({'status': 'Mensagem enviada com sucesso!'})

# Rota para carregar as mensagens existentes (para exibir no chat)
@chat_bp.route('/carregar_mensagens', methods=['GET'])
def carregar_mensagens():
    return jsonify(mensagens)
