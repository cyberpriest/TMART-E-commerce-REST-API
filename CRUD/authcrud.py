from sqlalchemy.orm import Session 
from schema import UserCreate
from fastapi import HTTPException,status
from models import User
from auth import gen_hash




def add_new_user(db:Session,data:UserCreate):
    user = User(
        **data.model_dump(exclude={'password'}),
        hashed_pw = gen_hash(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 


def me(db:Session,user:User):
    return db.query(User).filter(User.id == user.id).first()





