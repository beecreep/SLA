from flask import Flask, redirect, render_template, request, jsonify, url_for, send_from_directory,  send_file, session
import sqlite3
import io
import mimetypes
from materias import materias_bp


app = Flask(__name__)
app.secret_key = '12345678910'

app.register_blueprint(materias_bp)

# Função para conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect('usuarios.db')
    print("Conexão com banco de dados estabelecida")
    return conn

# Função para criar a tabela de usuários
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL,
                        senha TEXT NOT NULL,
                        turma TEXT,
                        numero TEXT,
                        role TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    arquivo BLOB,  -- Se o professor quiser enviar arquivos
    data_envio DATE DEFAULT (datetime('now', 'localtime')));''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS respostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER,
    atividade_id INTEGER,
    resposta TEXT,
    arquivo_resposta BLOB,
    data_resposta DATE DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (atividade_id) REFERENCES atividades(id));''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS mensagens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario_id INTEGER,
                        mensagem TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(usuario_id) REFERENCES usuarios(id))''')
    
    conn.commit()
    conn.close()

# Cria a tabela ao iniciar o servidor
create_table()

# Rota para servir o arquivo HTML (cadastro.html)
@app.route('/')
def index():
    return render_template('cadastro.html')

# Rota para ca dastrar um novo usuário
@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    
    nome = data['nome']
    email = data['email']
    senha = data['senha']
    turma = data.get('turma', '')
    numero = data.get('numero', '')
    role = data['role']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO usuarios (nome, email, senha, turma, numero, role)
                      VALUES (?, ?, ?, ?, ?, ?)''', (nome, email, senha, turma, numero, role))         
    
    conn.commit() 
    conn.close()

    return jsonify({'status': 'Usuário cadastrado com sucesso!'})

# Rota para fazer login
@app.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    email = data['email']
    senha = data['senha']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email=? AND senha=?', (email, senha))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Verifica o papel do usuário (Aluno ou Professor)
       nome = user[1]  # Pega o nome do usuário (segunda coluna)
       role = user[6]  # Pega o role (Aluno ou Professor)
        
    if role == 'Aluno':
            # Redireciona para aluno.html com o nome do usuário na URL
            return jsonify({
                'status': 'success',
                'redirect_url': f'/aluno/{nome}'
            })
    elif role == 'Professor':
            return jsonify({
                'status': 'success',
                'redirect_url': f'/professor/{nome}'
            })
    else:
        return jsonify({'status': 'Falha no login. Verifique suas credenciais.'})
    
#rotas para rederizar os sites
@app.route('/aluno/<nome>')
def aluno(nome):
    return render_template('aluno.html', nome=nome,)

@app.route('/professor/<nome>')
def professor(nome): 
      # Redireciona se não estiver autenticado como professor

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        arquivo = request.files['arquivo'].read() if 'arquivo' in request.files else None

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO atividades (titulo, descricao, arquivo) VALUES (?, ?, ?)',
                       (titulo, descricao, arquivo))
        conn.commit()
        conn.close()

        return "Atividade enviada com sucesso!"
    return render_template('professor.html', nome=nome )

@app.route('/logout')
def logout():
    session.clear()  # Limpa a sessão
    return redirect('/')  # Redireciona para a página inicial

@app.route('/chat')
def chat():
    conn = connect_db()
    cursor = conn.cursor()

    # Pegar todas as mensagens, juntamente com o nome do usuário
    cursor.execute('''
        SELECT usuarios.nome, mensagens.mensagem 
        FROM mensagens 
        JOIN usuarios ON mensagens.usuario_id = usuarios.id 
        ORDER BY mensagens.timestamp ASC
    ''')
    mensagens = cursor.fetchall()

    conn.close()

    # Renderizar o template do chat com as mensagens enviadas
    return render_template('chat.html', mensagens=mensagens)

@app.route('/pdf/view/<path:subpath>/<filename>')
def view_pdf(subpath, filename):
    # 'subpath' permite acessar subpastas
    return send_from_directory(f'pdfs/{subpath}', filename)

@app.route('/pdf/download/<path:subpath>/<filename>')
def download_pdf(subpath, filename):
    # 'subpath' permite acessar subpastas
    return send_from_directory(f'pdfs/{subpath}', filename, as_attachment=True)

@app.route('/download/<int:atividade_id>')
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

  #rota para professor enviar uma atividade
@app.route('/prof-atv', methods=['POST'])
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

@app.route('/enviar_resposta', methods=['POST'])
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

@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    conn = connect_db()
    cursor = conn.cursor()
    
    usuario_id = request.form['usuario_id']  # ID do usuário que está enviando a mensagem
    mensagem = request.form['mensagem']  # Mensagem enviada pelo usuário

    # Inserir a mensagem no banco de dados
    cursor.execute('INSERT INTO mensagens (usuario_id, mensagem) VALUES (?, ?)', (usuario_id, mensagem))
    conn.commit()

    # Pegar todas as mensagens para retornar ao frontend
    cursor.execute('SELECT usuarios.nome, mensagens.mensagem FROM mensagens JOIN usuarios ON mensagens.usuario_id = usuarios.id ORDER BY mensagens.data_hora ASC')
    todas_mensagens = cursor.fetchall()
    
    conn.close()

    # Retornar as mensagens como JSON para serem exibidas no chat
    return jsonify(todas_mensagens)

@app.route('/api/alunos', methods=['GET'])
def get_alunos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, turma FROM usuarios WHERE role = 'Aluno'")
    alunos = [{'nome': row[0], 'turma': row[1]} for row in cursor.fetchall()]
    conn.close()

    return jsonify(alunos=alunos)

# Rota para a página de atividades
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
@app.route('/atividade')
def atividade():
    atividades = obter_atividades()  # Obtém as atividades
    return render_template('atividade.html', atividades=atividades)


if __name__ == '__main__':
    app.run(debug=True)
