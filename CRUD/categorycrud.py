from sqlalchemy.orm import Session 
from fastapi import HTTPException,status


from schema import CategoryCreate,CategoryUpdate
from models import Category,User
from enums import UserRole # my roles 
from utils import paginate



def add_category(db:Session,data:CategoryCreate,user:User):
    addCategory = Category(
        **data.model_dump()
    )
    db.add(addCategory)
    db.commit()
    db.refresh(addCategory)
    return addCategory





def get_all_categories(db:Session,page:int=1 ,limit:int=10,search :str|None = None):
    query = db.query(Category)

    if search:
        query.filter(Category.name.ilike(f"%{search}%"))

    total_category  = query.count()
    page,limit = paginate.Paginate(page,limit)

    results = query.order_by(Category.created_at.desc()).offset(page).limit(limit).all()

    return {
        'total_category':total_category,
        'page':page,
        'limit':limit,
        'results':results
    }


def edit_category(db:Session,category_id:int,data:CategoryUpdate,user:User):
    cate = db.query(Category).filter(Category.id == category_id).first()
    if not cate:
        raise HTTPException(status_code=404,detail="cateory not found")


    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cate, key, value)
    db.commit()
    db.refresh(cate)
    return cate


def remove_category(db:Session,category_id:int,user:User):
    cate = db.query(Category).filter(Category.id == category_id).first()
    if not cate:
        raise HTTPException(status_code=404,detail="category not found")



    db.delete(cate)
    db.commit()
    return cate