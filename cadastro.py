from flask import Flask, redirect, render_template, request, jsonify, url_for, send_from_directory
import sqlite3

app = Flask(__name__)

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
      
        role = user[6]  # A posição do 'role' na tabela, provavelmente a 6ª coluna
        if role == 'Aluno':
             return jsonify({'status': 'success', 'redirect_url': '/aluno' })
        elif role == 'Professor':
            return jsonify({'status': 'success', 'redirect_url': '/professor'})
    else:
        return jsonify({'status': 'Falha no login. Verifique suas credenciais.'})
    
#rotas para rederizar os sites
@app.route('/aluno')
def aluno():
    return render_template('aluno.html')

@app.route('/professor')
def professor():
    return render_template('professor.html')

@app.route('/historia')
def historia():
    return render_template('materias.html/historia.html')

@app.route('/portugues')
def portugues():
    return render_template('materias.html/portugues.html')

@app.route('/geografia')
def geografia():
    return render_template('materias.html/geografia.html')

@app.route('/matematica')
def matematica():
    return render_template('materias.html/matematica.html')

@app.route('/fisica')
def fisica():
    return render_template('materias.html/fisica.html')

@app.route('/quimica')
def quimica():
    return render_template('materias.html/quimica.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/biologia')
def biologia():
    return render_template('materias.html/biologia.html')

@app.route('/ingles')
def ingles():
    return render_template('materias.html/ingles.html')

@app.route('/st')
def st():
    return render_template('materias.html/curso-sites/st.html')

@app.route('/adm')
def adm():
    return render_template('materias.html/curso-sites/adm.html')

@app.route('/eventos')
def eventos():
    return render_template('materias.html/curso-sites/eventos.html')

@app.route('/eletronica')
def eletronica():
    return render_template('materias.html/curso-sites/eletronica.html')

@app.route('/pdf/view/<path:subpath>/<filename>')
def view_pdf(subpath, filename):
    # 'subpath' permite acessar subpastas
    return send_from_directory(f'pdfs/{subpath}', filename)

@app.route('/pdf/download/<path:subpath>/<filename>')
def download_pdf(subpath, filename):
    # 'subpath' permite acessar subpastas
    return send_from_directory(f'pdfs/{subpath}', filename, as_attachment=True)

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

@app.route('/aluno-resposta', methods=['GET', 'POST'])
def alunoresposta():
    conn = get_db_connection()
    atividades = conn.execute('SELECT * FROM atividades').fetchall()
    conn.close()

    if request.method == 'POST':
        aluno_id = request.form['aluno_id']  # Supondo que o ID do aluno seja passado de alguma forma
        atividade_id = request.form['atividade_id']
        resposta = request.form['resposta']
        arquivo_resposta = request.files['arquivo_resposta'].read() if 'arquivo_resposta' in request.files else None
        
        conn = get_db_connection()
        conn.execute('INSERT INTO respostas (aluno_id, atividade_id, resposta, arquivo_resposta) VALUES (?, ?, ?, ?)',
                     (aluno_id, atividade_id, resposta, arquivo_resposta))
        conn.commit()
        conn.close()
        
        return redirect(url_for('aluno'))

    return render_template('aluno.html', atividades=atividades)

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

@app.route('/atividades', methods=['GET'])
def get_atividades():
    conn = connect_db()
    cursor = conn.cursor()

    # Seleciona todas as atividades
    cursor.execute('SELECT titulo, descricao FROM atividades')
    atividades = cursor.fetchall()
    conn.close()

    # Retorna as atividades como JSON
    return jsonify(atividades)


if __name__ == '__main__':
    app.run(debug=True)
