
from db import create_tables
from db import db  # Importa a instância de db do db.py
from cadastrar import cadastro_bp
from professor import professor_bp
from aluno import aluno_bp
from models import User  # Importe o modelo
from materias import materias_bp
from chat import chat_bp
from atividade import atividade_bp
from cadastro import cadastrar_usuario
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask, redirect, render_template, request, jsonify, url_for, session

app = Flask(__name__)
app.secret_key = '12345678910'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
app.register_blueprint(cadastro_bp, url_prefix='/cadastro')
app.register_blueprint(professor_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(materias_bp)
app.register_blueprint(atividade_bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria todas as tabelas definidas
    app.run(debug=True)
    
