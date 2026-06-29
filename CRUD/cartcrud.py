from sqlalchemy.orm import Session 
from schema import CartCreate ,CartUpdate
from fastapi import HTTPException

from models import User,Cart,CartItems,Product

from enums import UserRole # my roles 


def add_cart(db:Session,data:CartCreate,user:User):
    cart = Cart(
        owner_id=user.id,
    )
    db.add(cart)
    db.flush() 

    for  items in  data.items:
        product = db.query(Product).filter(Product.id == items.product_id,).first()
        if not product:
            raise HTTPException(status_code=404, detail=f'product {items.product_id} not found')
        if not product.is_available:
            raise HTTPException(status_code=400, detail=f'product {product.name} is not available')
        
        cartitem = CartItems(
            cart_id = cart.id,
            product_id = items.product_id)
        db.add(cartitem)
    db.commit()
    db.refresh(cart)
    return cart


def get_user_carts(db:Session,user:User):
    query = db.query(Cart)
    if user.role in [UserRole.STAFF, UserRole.ADMIN]:
        return query.all()
    return query.filter(Cart.owner_id == user.id).all()


def update_cart(db:Session,cart_id:int,data:CartUpdate,user:User):
    cart = db.query(Cart).filter(Cart.id == cart_id,Cart.owner_id == user.id).first()
    if not cart:
        raise HTTPException(status_code=404,detail="cart not found")
    is_authorized = user.role in [UserRole.STAFF, UserRole.ADMIN]
    if not is_authorized:
        raise HTTPException(status_code=401,detail="not authorized")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cart, key, value)
    db.commit()
    db.refresh(cart)
    return cart


def remove_cart(db:Session,cart_id:int,user:User):
    cart = db.query(Cart).filter(Cart.id == cart_id,Cart.owner_id == user.id).first()
    if not cart:
        raise HTTPException(status_code=404,detail="cart not found")
    is_authorized = user.role in [UserRole.STAFF, UserRole.ADMIN]
    if not is_authorized:
        raise HTTPException(status_code=403,detail="not authorized")

    db.delete(cart)
    db.commit()
    return cart