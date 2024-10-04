from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conectando ao banco de dados
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Conectado ao banco de dados com sucesso")
    
    # Adicionando a coluna 'role' (papel)
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT, 
                     email TEXT, 
                     role TEXT)''')
    print("Tabela criada com sucesso")
    conn.close()

init_sqlite_db()

# Rota principal (página de cadastro)
@app.route('/')
def index():
    return render_template('form.html')

# Rota para lidar com o envio do formulário (cadastro)
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']  # Capturando a escolha do input rádio

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (name, email, role) VALUES (?, ?, ?)", (name, email, role))
            con.commit()

        # Redireciona para a página de login após o cadastro
        return redirect(url_for('login'))

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE name = ? AND email = ?", (name, email))
            user = cur.fetchone()

            if user:
                role = user[3]  # Pegando o valor da coluna 'role' no banco de dados
                if role == 'professor':
                    return redirect(url_for('professor_dashboard', name=name))
                elif role == 'aluno':
                    return redirect(url_for('aluno_dashboard', name=name))
            else:
                msg = "Nome ou email incorreto. Tente novamente."

    return render_template('login.html', msg=msg)

# Dashboard do Professor
@app.route('/professor_dashboard/<name>')
def professor_dashboard(name):
    return render_template('prof.html', name=name)

# Dashboard do Aluno
@app.route('/aluno_dashboard/<name>')
def aluno_dashboard(name):
    return render_template('aluno.html', name=name)

# Rota de boas-vindas para usuários autenticados
@app.route('/welcome/<name>')
def welcome(name):
    return f"Bem-vindo, {name}!"

if __name__ == '__main__':
    app.run(debug=True)
