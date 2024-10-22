import sqlite3

def connect_db():
    conn = sqlite3.connect('usuarios.db')
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Criação das tabelas
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
                        arquivo BLOB,
                        data_envio DATE DEFAULT (datetime('now', 'localtime')))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS respostas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        aluno_id INTEGER,
                        atividade_id INTEGER,
                        resposta TEXT,
                        arquivo_resposta BLOB,
                        data_resposta DATE DEFAULT (datetime('now', 'localtime')),
                        FOREIGN KEY (atividade_id) REFERENCES atividades(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS mensagens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario_id INTEGER,
                        mensagem TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(usuario_id) REFERENCES usuarios(id))''')

    conn.commit()
    conn.close()
