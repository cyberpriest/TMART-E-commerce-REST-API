from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

BASE = declarative_base()  

SQL_URI = os.getenv("DATABASE_URL", "sqlite:///test.db")  # reads from .env, falls back to sqlite
engine = create_engine(SQL_URI, connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()