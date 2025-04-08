from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Blueprints e módulos internos
from db import db
from models import User
from cadastrar import cadastro_bp, cadastrar_usuario
from professor import professor_bp
from aluno import aluno_bp
from materias import materias_bp
from chat import chat_bp
from atividade import atividade_bp
from cronogramas import cronogramas_bp

# Inicialização da aplicação Flask
app = Flask(__name__)

# Configurações principais
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '12345678910')  # Idealmente, use variável de ambiente
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para uploads

# Inicializa extensões
db.init_app(app)
migrate = Migrate(app, db)

# Gerenciador de Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'cadastrar.login_usuario'  # Redireciona para login se não autenticado

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Criação do banco (somente se estiver vazio)
with app.app_context():
    if not os.path.exists('usuarios.db'):
        db.create_all()

# Rota principal
@app.route('/')
def index():
    return render_template('home_page.html')

# Rota de cadastro de usuário via formulário
@app.route('/cadastro', methods=['POST'])
def cadastro():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    resultado = cadastrar_usuario(username, password, role)
    if "sucesso" in resultado:
        return redirect(url_for('login'))
    return jsonify({"erro": resultado})

# Registro de todos os blueprints
app.register_blueprint(cadastro_bp,     url_prefix='/cadastrar')
app.register_blueprint(professor_bp,    url_prefix='/professor')
app.register_blueprint(aluno_bp,        url_prefix='/aluno')
app.register_blueprint(chat_bp,         url_prefix='/chat')
app.register_blueprint(materias_bp)
app.register_blueprint(atividade_bp,    url_prefix='/atividade')
app.register_blueprint(cronogramas_bp,  url_prefix='/cronogramas')

# Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000) # host permite que outras maquinas aceseem, port é a porta padrão
