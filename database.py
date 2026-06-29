from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine

import os




BASE = declarative_base()  

SQL_URI = 'sqlite:///test.db'
engine = create_engine(SQL_URI,connect_args={'check_same_thread':False},echo=True)
SessionLocal = sessionmaker(autoflush=False,autocommit=False ,bind=engine,expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
