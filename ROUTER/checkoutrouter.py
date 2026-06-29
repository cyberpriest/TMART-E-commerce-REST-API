from fastapi import APIRouter,Depends
from CRUD.checkoutcrud import checkout
from sqlalchemy.orm import Session
from database import get_db
from schema import OrderRead
from auth import get_current_user
from models import User




checkout_router = APIRouter(prefix='/checkout',tags = ['CHECKOUT'])


@checkout_router.post('/{cart_id}', response_model=OrderRead)
def checkout_cart(cart_id:int,db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    return checkout(db, cart_id,user)