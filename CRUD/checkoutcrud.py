from sqlalchemy.orm import Session 
from fastapi import HTTPException,status

from models import User,Cart,OrderItem,Product,Order






def checkout(db:Session,cart_id:int,user:User):
    cart = db.query(Cart).filter(
        Cart.id == cart_id ,
          Cart.owner_id == user.id
            ).first()
    if not cart :
        raise HTTPException(status_code=404,detail="not found")
    if  cart.is_checked_out :
        raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='cart already checked out')
    
    if not cart.items:
         raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='cart already checked out')


    order = Order(
        user_id = user.id,
        total = 0.0
        )
    db.add(order)
    db.flush() # used to get the cart_id 

    total = 0.0

    for item in cart.items:
        product = db.query(Product).filter(Product.id == item.product_id).first() 
        if not product:
            raise HTTPException(status_code=404, detail=f"not found")
        if not product.is_available:
            raise HTTPException(status_code=400, detail=f"{product.name} is not available")
        orderitems = OrderItem(
            order_id = order.id ,
            product_id = item.product_id,
            quantity = item.quantity,
            unit_price = product.price
            )
        total += product.price * item.quantity
        db.add(orderitems)
    order.total = total 
    cart.is_checked_out = True
    db.commit()
    db.refresh(order)
    return order
    


    


