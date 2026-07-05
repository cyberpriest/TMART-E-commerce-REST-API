from fastapi import APIRouter,Depends, File, UploadFile
from CRUD.productscrud import get_all_products,update_product,\
    remove_product,add_product,upload_product_image,product_detail
from sqlalchemy.orm import Session
from database import get_db
from schema import ProductCreate,ProductRead,ProductUpdate,ProductReadResponse
from auth import required_role
from models import User
from enums import UserRole


product_router = APIRouter(prefix='/products',tags = ['PRODUCTS'])



@product_router.get('/',response_model=ProductReadResponse)
def get_all_product(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10,
    search: str | None = None
):
    return get_all_products(db,page,limit,search)

@product_router.post('/create',response_model=ProductRead)
def  create_products(
        data:ProductCreate,
        db: Session = Depends(get_db),
        user:User = Depends(required_role(UserRole.ADMIN,UserRole.STAFF))
       
):
    return add_product(db,data,user)


@product_router.delete('/delete/{product_id}',response_model=ProductRead)
def  delete_products(
        product_id: int,
        db: Session = Depends(get_db),
        user:User = Depends(required_role(UserRole.ADMIN))
       
):
    return remove_product(db,product_id,user)


@product_router.patch('/update/{product_id}',response_model=ProductRead)
def edit_products(
        product_id: int,
        data:ProductUpdate,
        db: Session = Depends(get_db),
        user:User = Depends(required_role(UserRole.ADMIN))
       
):
    return update_product(db,product_id,data,user)

@product_router.get('/detail/{product_id}',response_model=ProductRead)
def product_details(db: Session = Depends(get_db),product_id:int = 1):
    return product_detail(db,product_id)

@product_router.post('/upload-image/{product_id}',response_model=ProductRead)
def upload_product_images(
        product_id: int,
        image_url: UploadFile = File(..., description="Upload an image file"),
        db: Session = Depends(get_db),
        user:User = Depends(required_role(UserRole.ADMIN,UserRole.STAFF))
       
):
    return upload_product_image(db,product_id,image_url,user)