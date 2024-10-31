from flask import Flask, redirect, render_template, request, jsonify, url_for, session, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db, User


cadastro_bp = Blueprint ('cadastrar', __name__)

app = Flask(__name__)
app.secret_key = '12345678910'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'  

# Classe para usuários (UserMixin é necessário para o Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota para ca dastrar um novo usuário
@cadastro_bp.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    senha = generate_password_hash(data['senha'])
    turma = data.get('turma', '')
    numero = data.get('numero', '')
    role = data['role']

    novo_usuario = User(nome=nome, email=email, senha=senha, turma=turma, numero=numero, role=role)
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({'status': 'Usuário cadastrado com sucesso!'})

# Rota para fazer login
@cadastro_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    email = data['email']
    senha = data['senha']

    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.senha, senha):
        login_user(user)
        redirect_url = '/aluno' if user.role == 'Aluno' else '/professor'
        return jsonify({'status': 'success', 'redirect_url': redirect_url})
    else:
        return jsonify({'status': 'Falha no login. Verifique suas credenciais.'}), 401
#rotas para rederizar os sites
@cadastro_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')  # Redireciona para a página inicial

if __name__ == '__main__':
    app.run(debug=True)
