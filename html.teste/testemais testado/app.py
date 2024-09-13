import sqlite3

# Conexão ao banco de dados
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criando a tabela de usuários
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
''')

# Função para adicionar um novo usuário
def adicionar_usuario(nome):
    cursor.execute('INSERT INTO usuarios (nome) VALUES (?)', (nome,))
    conn.commit()

# Função para buscar um usuário
def buscar_usuario(nome):
    cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (nome,))
    return cursor.fetchone()

# Fechando a conexão
conn.close()
