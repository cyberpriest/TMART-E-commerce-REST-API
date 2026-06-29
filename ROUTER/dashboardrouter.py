from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import required_role
from models import User
from enums import UserRole
from CRUD.dashboardcrud import overview ,product_list
from schema import ProductRead



dashboard_router = APIRouter(prefix='/dashboard',tags = ['ADMIN-DASHBOARD'])


@dashboard_router.get('/')
def Over_view(db:Session = Depends(get_db),user:User = Depends(required_role(UserRole.ADMIN))):
    return overview(db,user)
    
@dashboard_router.get('/product-list',response_model = list[ProductRead])
def all_products(db:Session = Depends(get_db),user:User = Depends(required_role(UserRole.ADMIN))):
    return product_list(db,user)