from fastapi import APIRouter ,Depends,HTTPException,status
import schema,database,models,auth
from sqlalchemy.orm import Session
from CRUD.authcrud import add_new_user,me
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix='/auth',tags=['AUTHENTICATION'])





@auth_router.post('/register',response_model=schema.UserRead)
def create_user(data:schema.UserCreate,db:Session  =  Depends(database.get_db)):
   
    is_exist = db.query(models.User).filter(models.User.email == data.email).first()
    if is_exist:
        raise HTTPException(status_code=403,detail='exists')
    user =  add_new_user(db,data)
    return user



@auth_router.post('/login',response_model=schema.TokenResponse)
def login(data:OAuth2PasswordRequestForm =Depends(),db:Session  =  Depends(database.get_db)):
    user = auth.authenticate(db,data.username,data.password)
    createtoken = auth.create_token({'sub':user.email})
    refreshtoken = auth.create_refresh_token({'sub':user.email})

    return {'access_token':createtoken,'access_type':'bearer','refresh_token':refreshtoken}

@auth_router.get('/me/profile',response_model=schema.UserRead)
def Me(db:Session  =  Depends(database.get_db),user:models.User = Depends(auth.get_current_user)):
    return me(db,user)
