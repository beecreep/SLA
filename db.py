import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db():
    db.create_all()

Base = declarative_base()
engine = create_engine('sqlite:///usuarios.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def connect_db():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'usuarios.db')
    conn = sqlite3.connect(db_path)
    return conn