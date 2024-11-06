
from db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin


mensagens = relationship("Mensagem", back_populates="user", cascade="all, delete-orphan")

user = relationship("User", back_populates="mensagens")

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    turma = db.Column(db.String(50))
    numero = db.Column(db.String(50))
    role = db.Column(db.String(50))

    mensagens = db.relationship('Mensagem', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.nome}>'
    
class Atividade(db.Model):
    __tablename__ = 'atividades'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    arquivo = db.Column(db.LargeBinary)  # Store files as binary
    data_envio = db.Column(db.DateTime, default=db.func.current_timestamp())

class Resposta(db.Model):
    __tablename__ = 'respostas'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)
    resposta = db.Column(db.Text, nullable=False)
    arquivo_resposta = db.Column(db.LargeBinary)
    data_resposta = db.Column(db.DateTime, default=db.func.current_timestamp())

class Mensagem(db.Model):
    __tablename__ = 'mensagens'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', back_populates='mensagens')

    def __repr__(self):
        return f'<Mensagem {self.id}: {self.mensagem}>'


