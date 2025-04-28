#import sqlite3
#from sqlalchemy import create_engine
#from sqlalchemy.orm import declarative_base
#from sqlalchemy.orm import sessionmaker

#intermedia a aplicação com o banco de dados
from flask_sqlalchemy import SQLAlchemy 
import os

db = SQLAlchemy() #coração do banco de dados, onde ele vai fazer a conexão com o banco de dados e criar as tabelas e tudo mais.
#o SQLAlchemy é uma biblioteca ORM (Object Relational Mapper) para Python que facilita a interação com bancos de dados relacionais. Ele permite que você trabalhe com bancos de dados usando objetos Python em vez de escrever consultas SQL diretamente.

def init_db(app):
     with app.app_context():
        db.init_app(app)
      #  db.create_all()