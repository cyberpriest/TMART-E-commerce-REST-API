from fastapi import APIRouter,Depends
from CRUD.ordercrud import remove_order,get_all_orders,edit_order
from sqlalchemy.orm import Session
from database import get_db
from schema import OrderCreate,OrderRead,OrderUpdate,OrderReadResponse
from auth import required_role,get_current_user
from models import User
from enums import UserRole



order_router = APIRouter(prefix='/order',tags = ['ORDER'])


@order_router.get('/', response_model=OrderReadResponse)
def list_orders(
        page:int = 1,
        limit:int  = 10,
    # search:str|None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return get_all_orders(db, user)


# @order_router.post('/create', response_model=OrderRead)
# def create_order(
#     data: OrderCreate,
#     db: Session = Depends(get_db),
#     user: User = Depends(get_current_user)
# ):
#     return add_order(db, data,user)


@order_router.patch('/{order_id}', response_model=OrderRead)
def update_order(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    pass
    return edit_order(db, order_id, data, user)


@order_router.delete('/{order_id}', response_model=OrderRead)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return remove_order(db, order_id, user)
