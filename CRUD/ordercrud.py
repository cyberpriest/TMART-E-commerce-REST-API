from sqlalchemy.orm import Session 
from fastapi import HTTPException,status

from models import User,Order,OrderItem,User,Product
from enums import UserRole,OrderStatus # my roles 
from utils import paginate
from schema import OrderCreate,OrderUpdate

VALID_TRANSITIONS = {
    OrderStatus.PENDING:    [OrderStatus.PAID, OrderStatus.CANCELLED],
    OrderStatus.PAID:       [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
    OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED:    [OrderStatus.DELIVERED, OrderStatus.RETURNED],
    OrderStatus.DELIVERED:  [OrderStatus.RETURNED],
    OrderStatus.CANCELLED:  [],
    OrderStatus.RETURNED:   [],
}





def get_all_orders(db:Session,user:User,page:int=1 ,limit:int=10):
    query = db.query(Order)

    if user.role in [UserRole.STAFF, UserRole.ADMIN]:
        query.all()
    query = db.query(Order).filter(Order.user_id == user.id)

    
    total_order  = query.count()
    page,limit = paginate.Paginate(page,limit)

    results = query.order_by(Order.created_at.desc()).offset(page).limit(limit).all()

    return {
        'total_order':total_order,
        'page':page,
        'limit':limit,
        'results':results
    }


def edit_order(db:Session,order_id:int,data:OrderUpdate,user:User):
    order = db.query(Order).filter(Order.id == order_id,Order.user_id == user.id).first()
    

    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    
    if data.status is not None:
        allow = VALID_TRANSITIONS.get(order.status,[])
        if data.status not in allow:
            raise HTTPException(status_code=400,detail=f"cant move order from   {order.status}to  {data.status} ")





    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order


def remove_order(db:Session,order_id:int,user:User):
    order = db.query(Order).filter(Order.id == order_id,Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404,detail="order not found")



    db.delete(order)
    db.commit()
    return order