
from database import BASE,engine,SessionLocal
from sqlalchemy.orm import Session
from collections import deque 
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import faker, json, random
from slugify import slugify
from auth import gen_hash
from pathlib import Path

from models import User , Product ,Category
from enums import UserRole
fake = faker.Faker()


# base paths
_base_dir = Path(__file__).resolve().parent
_dump_file_path = _base_dir / 'utils' / 'logs.json'
# _images_dir = _base_dir / 'static' / 'products'
# _images_dir.mkdir(parents=True, exist_ok=True)
# IMAGE_BASE_URL = '/static/products'


#============================================================
#                       SEEDING DUMMY DATA
#============================================================

def run_db():
    BASE.metadata.drop_all(bind=engine)
    BASE.metadata.create_all(bind=engine)



def seed_admin(db):
    admin_arr = list()

    admin = User(
        email = "joshuatimi41@gmail.com",
        full_name  = "John Doe",
        hashed_pw = gen_hash('password123'),
        role =  UserRole.ADMIN

    )

    db.add(admin)
    db.commit()
    admin_arr.append(admin)
    print(f"{admin_arr} as being created successfully !")
    return admin_arr


def seed_staff(db):
    staff_arr = list()

    staff = User(
        email = "mystaff@email.com",
        full_name  = "staff Doe",
        hashed_pw = gen_hash('password123'),
        role =  UserRole.STAFF

    )

    db.add(staff)
    db.commit()
    staff_arr.append(staff)
    print(f"{staff_arr} as being created successfully !")
    return staff_arr



def seed_customer(db,count:int = 5):
    costumer_arr = list()

    for _ in range(count):

        customer = User(
            email = fake.email(),
            full_name  = fake.name(),
            hashed_pw = gen_hash('password123'))
        db.add(customer)
        costumer_arr.append(customer)
    db.commit()
    
    print(f"{costumer_arr} as being created successfully !")
    return costumer_arr


def write_logs(data):
  
    with  open(_dump_file_path,'w') as  dump_file_path:
        json_data = json.dump(jsonable_encoder(data,exclude={'hashed_pw'}),dump_file_path,indent=5)
        return JSONResponse(content={'status':'sucesss','data':json_data,'status_code':200})
        
    

# def compress_product_image(name: str) -> str:
#     try:
#         from PIL import Image
#         from PIL.Image import Resampling
#     except ImportError:
#         return fake.image_url()

#     filename = f"{slugify(name)}-{fake.random_number(digits=5)}.jpg"
#     output_path = _images_dir / filename
#     image = Image.new(
#         'RGB',
#         (1200, 1200),
#         (
#             fake.random_int(min=0, max=255),
#             fake.random_int(min=0, max=255),
#             fake.random_int(min=0, max=255),
#         ),
#     )
#     image = image.resize((640, 640), Resampling.LANCZOS)
#     image.save(output_path, format='JPEG', quality=25, optimize=True, progressive=True)
#     return f"{IMAGE_BASE_URL}/{filename}"


def seed_categories(db):
    category_names = ['Electronics', 'Clothing', 'Food & Drinks', 'Home & Kitchen']
    categories = []
    for name in category_names:
        category = Category(
            name=name,
            slug=name.lower().replace(' ', '-').replace('&', 'and')
        )
        db.add(category)
        categories.append(category)
    db.commit()
    print(f"{len(categories)} categories created successfully!")
    return categories


def seed_products(db, categories, count: int = 5):
    products = []
    for category in categories:
        for _ in range(count):
            product_name = f"{fake.color_name()} {fake.word().capitalize()}"
            product = Product(
                name=product_name,
                description=fake.sentence(),
                price=round(fake.random_number(digits=4), 2),
                is_available=fake.boolean(chance_of_getting_true=80),
                category_id=category.id,
                image_url = None
                # image_url=compress_product_image(product_name)
            )
            db.add(product)
            products.append(product)
    db.commit()
    print(f"{len(products)} products created successfully!")
    return products

    

def run():
    run_db()
    db:Session = SessionLocal()
    try :
        a = seed_admin(db)
        s = seed_staff(db)
        c = seed_customer(db)
        ct = seed_categories(db)
        p = seed_products(db,ct)
        
        
        write_logs([a,s,c,ct,p])
    finally:
        db.close()


if __name__ == '__main__':
    run()




