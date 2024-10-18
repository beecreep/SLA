from flask import Flask, redirect, render_template, request, jsonify, url_for
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

# Rota para cadastrar um novo usuário
@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    
    nome = data['nome']
    email = data['email']
    senha = data['senha']
    turma = data.get('turma', '')
    numero = data.get('numero', '')
    role = data['role']

    if '@' not in email or '.' not in email.split('@')[-1]:
            return "Email inválido!", 400  # Retorna um erro se o email for inválido

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
            return jsonify({'status': 'success', 'redirect_url': '/aluno'})
        elif role == 'Professor':
            return jsonify({'status': 'success', 'redirect_url': '/professor'})
    else:
        return jsonify({'status': 'Falha no login. Verifique suas credenciais.'})
    
#rotas para rederizar os sites

@app.route('/chat')
def chat():
    return render_template('chat.html')

#parte para implementar o chat
@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    data = request.get_json()
    usuario_id = data['usuario_id']
    mensagem = data['mensagem']

    # Recupera o nome do usuário com base no ID
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM usuarios WHERE id=?', (usuario_id,))
    nome_usuario = cursor.fetchone()[0]
    conn.close()

    # Cria a mensagem com o nome do usuário e a mensagem
    mensagem_formatada = {
        'usuario': nome_usuario,
        'mensagem': mensagem
    }

    # Adiciona à lista de mensagens
    mensagens.append(mensagem_formatada)

    return jsonify({'status': 'Mensagem enviada com sucesso!'})

  #rota para professor enviar uma atividade
@app.route('/professor', methods=['GET', 'POST'])
def professor():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        arquivo = request.files['arquivo'].read() if 'arquivo' in request.files else None
        
        conn = get_db_connection()
        conn.execute('INSERT INTO atividades (titulo, descricao, arquivo) VALUES (?, ?, ?)',
                     (titulo, descricao, arquivo))
        conn.commit()
        conn.close()

    atividades = conn.execute('SELECT * FROM atividades').fetchall()
        
    respostas = conn.execute('''
        SELECT r.id, u.nome AS aluno_nome, a.titulo AS atividade_titulo, r.resposta, r.data_resposta
        FROM respostas r
        JOIN usuarios u ON r.aluno_id = u.id
        JOIN atividades a ON r.atividade_id = a.id
    ''').fetchall()

    conn.close()

    return render_template('professor.html', atividades=atividades, respostas=respostas)

@app.route('/aluno', methods=['GET', 'POST'])
def aluno():
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


if __name__ == '__main__':
    app.run(debug=True)
