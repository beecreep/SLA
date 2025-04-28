
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
    respostas = db.relationship('Resposta', back_populates='user')
    cronogramas = db.relationship('Cronograma', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.nome}>'
    
class Atividade(db.Model):
    __tablename__ = 'atividades'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    arquivo = db.Column(db.LargeBinary)  # Store files as binary
    extensao = db.Column(db.String(10)) 
    data_envio = db.Column(db.DateTime, default=db.func.current_timestamp())

    respostas = db.relationship('Resposta', back_populates='atividade')

class Resposta(db.Model):
    __tablename__ = 'respostas'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)
    resposta = db.Column(db.Text, nullable=False)
    arquivo_resposta = db.Column(db.LargeBinary)
    extensao = db.Column(db.String(10))
    data_resposta = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', back_populates='respostas')
    atividade = db.relationship('Atividade', back_populates='respostas')

class Mensagem(db.Model):
    __tablename__ = 'mensagens'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=True)  # Pode ser nula, pois pode conter apenas arquivo
    arquivo = db.Column(db.LargeBinary, nullable=True)  # Para armazenar o arquivo
    extensao = db.Column(db.String(10), nullable=True)  # Para armazenar a extensão do arquivo
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', back_populates='mensagens')

    def __repr__(self):
        return f'<Mensagem {self.id}: {self.mensagem}>'
    
class Cronograma(db.Model):
    __tablename__ = 'cronogramas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    turma = db.Column(db.String(50), nullable=False)  # Nome ou ID da turma
    dia_semana = db.Column(db.String(50), nullable=False)  # Segunda, Terça, etc.
    horario = db.Column(db.String(10), nullable=False)  # Ex.: "08:00"
    aula = db.Column(db.String(150), nullable=True)  # Nome da matéria ou atividade
    professor = db.Column(db.String, nullable=False)

    user = db.relationship('User', back_populates='cronogramas')




