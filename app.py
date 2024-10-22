from flask import Flask,render_template
from db import create_tables
from auth import auth_bp
from professor import professor_bp
from aluno import aluno_bp
from chat import chat_bp


app = Flask(__name__)

# Cria as tabelas do banco de dados
create_tables()

@app.route('/')
def index():
    return render_template('cadastro.html')

# Registra os blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(professor_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(chat_bp)


if __name__ == '__main__':
    app.run(debug=True)
