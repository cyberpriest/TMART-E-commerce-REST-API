from fastapi import APIRouter,Depends
from CRUD.cartcrud import add_cart, get_user_carts, update_cart, remove_cart
from sqlalchemy.orm import Session
from database import get_db
from schema import Cart, CartCreate, CartUpdate
from auth import get_current_user
from models import User
from enums import UserRole


cart_router = APIRouter(prefix='/carts',tags = ['CART'])


@cart_router.get('/', response_model=list[Cart])
def list_carts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return get_user_carts(db, user)


@cart_router.post('/create', response_model=Cart)
def create_cart(
    data: CartCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return add_cart(db, data, user)


@cart_router.patch('/{cart_id}', response_model=Cart)
def edit_cart(
    cart_id: int,
    data: CartUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return update_cart(db, cart_id, data, user)


@cart_router.delete('/{cart_id}', response_model=Cart)
def delete_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return remove_cart(db, cart_id, user)
