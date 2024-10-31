from flask import  request, redirect, url_for, render_template, Blueprint,  send_file
import mimetypes
import io
import sqlite3

atividade_bp = Blueprint('atividade', __name__)

def connect_db():
    conn = sqlite3.connect('usuarios.db')
    print("Conexão com banco de dados estabelecida")
    return conn

@atividade_bp.route('/prof-atv', methods=['POST'])
def professor_atv():
    # Verifica se o referer é a página 'professor.html'
    referer = request.headers.get("Referer")
    if referer and '/professor' in referer:
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        arquivo = request.files['arquivo'].read() if 'arquivo' in request.files else None

        conn = connect_db()
        conn.execute('INSERT INTO atividades (titulo, descricao, arquivo) VALUES (?, ?, ?)',
                     (titulo, descricao, arquivo))
        conn.commit()
        conn.close()

        return redirect(url_for('professor'))  # Redireciona de volta para professor.html
    else:
        return "Ação não permitida", 403  # Código de status HTTP 403 para acesso proibido

@atividade_bp.route('/enviar_resposta', methods=['POST'])
def enviar_resposta():
    aluno_id = request.form['aluno_id']
    atividade_id = request.form['atividade_id']
    resposta = request.form['resposta']
    arquivo_resposta = request.files['arquivo_resposta'].read() if 'arquivo_resposta' in request.files else None

    conn = connect_db()
    cursor = conn.cursor()

    # Insere a resposta do aluno no banco de dados
    cursor.execute('''
        INSERT INTO respostas (aluno_id, atividade_id, resposta, arquivo_resposta) 
        VALUES (?, ?, ?, ?)
    ''', (aluno_id, atividade_id, resposta, arquivo_resposta))
    
    conn.commit()
    conn.close()

    return redirect(f'/atividade/{aluno_id}')

# Função para buscar as atividades do banco de dados
def obter_atividades():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Seleciona a coluna 'extensao' para saber o tipo do arquivo
    cursor.execute('SELECT id, titulo, descricao, data_envio, arquivo, extensao FROM atividades')
    atividades = cursor.fetchall()

    lista_atividades = []
    for atividade in atividades:
        lista_atividades.append({
            'id': atividade[0],
            'titulo': atividade[1],
            'descricao': atividade[2],
            'data_envio': atividade[3],
            'arquivo': atividade[4],
            'extensao': atividade[5]  # Adiciona a extensão do arquivo ao dicionário
        })

    conn.close()
    return lista_atividades

# Rota para exibir as atividades
@atividade_bp.route('/atividade')
def atividade():
    atividades = obter_atividades()  # Obtém as atividades
    return render_template('atividade.html', atividades=atividades)

@atividade_bp.route('/download/<int:atividade_id>')
def download(atividade_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT arquivo, extensao FROM atividades WHERE id=?', (atividade_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        arquivo, extensao = result
        mime_type, _ = mimetypes.guess_type(f"arquivo.{extensao}")
        
        return send_file(io.BytesIO(arquivo), as_attachment=True, 
                         download_name=f"arquivo_{atividade_id}.{extensao}", 
                         mimetype=mime_type)
    else:
        return "Arquivo não encontrado.", 404