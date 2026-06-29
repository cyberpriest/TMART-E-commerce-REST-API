from datetime import datetime
from pydantic import BaseModel,ConfigDict
from enums import UserRole, UserStatus, OrderStatus
from typing import Optional

#============================================================
#                         USERBASE
#============================================================
class UserBase(BaseModel):
    email: str
    full_name: str



class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


#============================================================
#                         ORDERITEMS
#============================================================


    
    


class  OrderItemsCreate(BaseModel):
    quantity:int = 1
    product_id:int
   
class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    model_config = ConfigDict(from_attributes=True)



#============================================================
#                         ORDERBASE
#============================================================
class OrderBase(BaseModel):
  
    items:list[OrderItemsCreate]



class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
   status :OrderStatus|None = None


class OrderRead(BaseModel):
    id: int
    user_id: int
    total:int
    items:list[OrderItemRead]
    created_at: datetime
    status :OrderStatus
    model_config = ConfigDict(from_attributes=True)

class OrderReadResponse(BaseModel):
    total_order:int
    page:int
    limit:int
    results:list[OrderRead]
    model_config = ConfigDict(from_attributes=True)

#============================================================
#                         PRODUCT
#============================================================
class Product(BaseModel):
    name:str
    description:str
    price:float
    is_available:bool



class ProductCreate(Product):
    category_id:int


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None
    is_available: bool | None = None

class ProductRead(BaseModel):
    id:int
    category_id:int
    name:str
    description:str
    is_available:bool
    price:float
    model_config = ConfigDict(from_attributes=True)

class ProductReadResponse(BaseModel):
    
        total_product:int
        page:int
        limit:int
        results:list[ProductRead]    
        model_config = ConfigDict(from_attributes=True)
#============================================================
#                         CATEGORY-BASE
#============================================================

class Category(BaseModel):
    name:str
  

class CategoryCreate(Category):
    pass


class CategoryUpdate(BaseModel):
    name:str|None = None


class CategoryRead(BaseModel):
    id:int
    name:str
    slug:str
    products:list[ProductRead]
    model_config = ConfigDict(from_attributes=True)

class CategoryReadResponse(BaseModel):
        total_category:int
        page:int
        limit:int
        results:list[CategoryRead]
        model_config = ConfigDict(from_attributes=True)













#============================================================
#                         LOGIN TOKEN-RESPONSE
#============================================================
class TokenResponse(BaseModel):
    access_token:str
    refresh_token: str
    token_type:str = 'bearer'




#============================================================
#                         CARTITEMS
#============================================================


class CartItemsCreate(BaseModel):
    product_id:int
    quantity:int


class CartItems(BaseModel):
    id:int
    cart_id:int
    product_id:int
    quantity:int
    created_at:datetime
    product:ProductRead
    model_config = ConfigDict(from_attributes=True)

#============================================================
#                         CART
#============================================================

class Cart(BaseModel):
    id:int
    is_checked_out:bool = False
    created_at:datetime
    items : list[CartItems]
    model_config = ConfigDict(from_attributes=True)



class CartCreate(BaseModel):
    # is_checked_out: bool = False
    items: list[CartItemsCreate]


class CartUpdate(BaseModel):
    is_checked_out: bool | None = None


class CartRead(BaseModel):
    class Config:
        from_attributes = True