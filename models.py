
from db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "Aluno" ou "Professor"

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
    
    def __repr__(self):
        return f'<User {self.username}>'
    # models.py

mensagens = relationship("Mensagem", back_populates="user", cascade="all, delete-orphan")

class Mensagem(db.Model):
    __tablename__ = 'mensagens'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('users.id'))
    mensagem = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="mensagens")

    def __repr__(self):
        return f'<Mensagem {self.id}: {self.mensagem}>'

