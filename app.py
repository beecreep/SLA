
from db import db  # Importa a instância de db do db.py
from cadastrar import cadastro_bp, cadastrar_usuario
from professor import professor_bp
from aluno import aluno_bp
from models import Mensagem, User, Atividade, Resposta 
from materias import materias_bp
from chat import chat_bp
from atividade import atividade_bp
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '12345678910'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'cadastrar.login_usuario'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

with app.app_context():
    db.create_all()  # Cria todas as tabelas

@app.route('/cadastro', methods=['POST'])
def cadastro():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    
    resultado = cadastrar_usuario(username, password, role)
    if "sucesso" in resultado:
        return redirect(url_for('login'))
    else:
        return jsonify({"erro": resultado})

# Cria as tabelas do banco de dados

@app.route('/')
def index():
    return render_template('cadastro.html')

# Registra os blueprints
app.register_blueprint(cadastro_bp,  url_prefix='/cadastrar')
app.register_blueprint(professor_bp,  url_prefix='/professor')
app.register_blueprint(aluno_bp,  url_prefix='/aluno')
app.register_blueprint(chat_bp,  url_prefix='/chat')
app.register_blueprint(materias_bp)
app.register_blueprint(atividade_bp,  url_prefix='/atividade')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria todas as tabelas definidas
    app.run(debug=True)
    
