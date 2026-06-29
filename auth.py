from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from database import get_db
from models import User
from enums import UserStatus,UserRole

SECRET_KEY = 'secret-key'
REFRESH_SECRET_KEY = 'REFRESH_SECRET_KEY'

bcrypt = CryptContext(schemes=['bcrypt'], deprecated='auto')
pwdbearer = OAuth2PasswordBearer(tokenUrl='auth/login')








def gen_hash(pwd:str):
    return bcrypt.hash(pwd)

def verify_pwd(plain_pwd:str,hash_pwd:str)->bool:
    return bcrypt.verify(plain_pwd,hash_pwd)

def authenticate(db:Session,email:str,password:str):
    user = db.query(User).filter(User.email == email).first()
    if not  user:
        raise HTTPException(status_code=404,detail='user not found')
    
    if not verify_pwd(password,user.hashed_pw):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid creds')
    
    return user




def create_token(data:dict):
    to_encode = data.copy()
    to_encode.update({'exp':datetime.now(tz=UTC) + timedelta(minutes=50)}) 
    return jwt.encode(to_encode,SECRET_KEY,algorithm="HS256")

def decode_token(token:str):
    return jwt.decode(token,SECRET_KEY,algorithms=["HS256"])


def get_current_user(db:Session = Depends(get_db), token:str = Depends(pwdbearer)):
    HTTP_Exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='NOT  AUTHORIZED',
        headers={'WWW-AUTHENTICATE':'bearer'}

    )

    try:
        payload = decode_token(token)
        email = payload.get('sub')
        if email is None:
            raise HTTP_Exception

    except JWTError :
        raise HTTP_Exception
    user = db.query(User).filter(User.email == email).first()
    if not user or user.status != UserStatus.ACTIVE:
        raise HTTP_Exception
    return user



def create_refresh_token(data:dict):
    to_encode = data.copy()
    to_encode.update({'exp':datetime.now(tz=UTC) + timedelta(days=7)}) 
    return jwt.encode(to_encode,REFRESH_SECRET_KEY,algorithm="HS256")

    
def refresh_token(db:Session = Depends(get_db), token:str = Depends(pwdbearer)):
    HTTP_Exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='NOT  AUTHORIZED',
        headers={'WWW-AUTHENTICATE':'bearer'}

    )

    try:
        payload = jwt.decode(token,REFRESH_SECRET_KEY,algorithms=['HS256'])
        email = payload.get('sub')
        if email is None:
            raise HTTP_Exception

    except JWTError :
        raise HTTP_Exception
    user = db.query(User).filter(User.email == email).first()
    if not user or user.status != UserStatus.ACTIVE:
        raise HTTP_Exception
    return user


def required_role(*role:UserRole):
    def check_role(user:User = Depends(get_current_user)):
        if user.role not in  role :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user
    return check_role


