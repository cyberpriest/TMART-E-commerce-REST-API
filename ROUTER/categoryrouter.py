from fastapi import APIRouter,Depends
from CRUD.categorycrud import add_category,edit_category,remove_category,get_all_categories
from sqlalchemy.orm import Session
from database import get_db
from schema import Category,CategoryCreate,CategoryRead,CategoryUpdate,CategoryReadResponse
from auth import required_role
from models import User
from enums import UserRole


category_router = APIRouter(prefix='/category',tags = ['PRODUCT-CATEGORY'])


@category_router.get('/', response_model=CategoryReadResponse)
def list_cartegory(
    db: Session = Depends(get_db),
    page:int = 1,
    limit:int  = 10,
    search:str|None = None,
    user: User = Depends(required_role(UserRole.STAFF, UserRole.ADMIN))
):
    return get_all_categories(db,page,limit,search)


@category_router.post('/create', response_model=CategoryRead)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(required_role(UserRole.STAFF, UserRole.ADMIN))
):
    return add_category(db, data, user)


@category_router.patch('/{category_id}', response_model=CategoryRead)
def edit_cart(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(required_role(UserRole.STAFF, UserRole.ADMIN))
):
    return edit_category(db, category_id, data, user)


@category_router.delete('/{category_id}', response_model=CategoryRead)
def delete_cart(
    category_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(required_role(UserRole.STAFF, UserRole.ADMIN))
):
    return remove_category(db, category_id, user)
