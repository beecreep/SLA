import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        senha TEXT NOT NULL,
                        turma TEXT,
                        numero TEXT,
                        role TEXT NOT NULL)''')
    
    # Tabela de arquivos (opcional, se houver necessidade de armazenar arquivos)
  

    conn.commit()
    conn.close()

init_db()
