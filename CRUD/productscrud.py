from sqlalchemy.orm import Session 
from schema import ProductCreate,ProductUpdate
from fastapi import HTTPException ,UploadFile
from models import Product,User,Category
from utils.paginate import Paginate
from utils.image import compress_image





def add_product(db:Session,data:ProductCreate,user:User):
    product = Product(
        **data.model_dump()
        )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product



def update_product(db:Session,product_id:int,data:ProductUpdate,user:User):
    # i will use require_role in my route for permissions
    product = db.query(Product).filter(
        Product.id == product_id
        ).first() # product object
    if not product:
        raise HTTPException(status_code=404,detail='product not found')
    
    for k,v in  data.model_dump(exclude_unset=True).items():
        setattr(product,k,v)

    db.commit()
    db.refresh(product)
    return product



def remove_product(db:Session,product_id:int,user:User):
    product = db.query(Product).filter(Product.id == product_id).first() # product object
    if not product:
        raise HTTPException(status_code=404,detail='product not found')
    
    db.delete(product)
    db.commit()
    return product



def product_detail(db:Session,product_id:int):
    product = db.query(Product).filter(Product.id == product_id).first() # product object
    if not product:
        raise HTTPException(status_code=404,detail='product not found')
    
    return product


def upload_product_image(db:Session,product_id:int,image_url:UploadFile,user:User):
    product = db.query(Product).filter(Product.id == product_id).first() # product object
    if not product:
        raise HTTPException(status_code=404,detail='product not found')
    upload_file = compress_image(image_url)
    
    product.image_url = upload_file
    db.commit()
    db.refresh(product)
    return product


def get_all_products(db:Session,page:int=1 ,limit:int=10,search :str|None = None):
    query = db.query(Product)

    if search:
        query.filter(Product.name.ilike(f"%{search}%"))

    total_product  = query.count()
    page,limit = Paginate(page,limit)

    results = query.order_by(Product.created_at.desc()).offset(page).limit(limit).all()

    return {
        'total_product':total_product,
        'page':page,
        'limit':limit,
        'results':results
    }



