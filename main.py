from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import BASE,engine
from ROUTER.authrouter import auth_router
from ROUTER.cartrouter import cart_router
from ROUTER.productsrouter import product_router
from ROUTER.orderrouter import order_router
from ROUTER.categoryrouter import category_router
from ROUTER.dashboardrouter import dashboard_router
from ROUTER.checkoutrouter import checkout_router
from PAYMENT.paymentrrouter import payment_router
app = FastAPI(
    title="TMART",
    description="""
🛒 **TMART** — A modern e-commerce API built with FastAPI.

**Features:**
- Auth with JWT & refresh tokens
- Product & category management
- Cart & checkout flow
- Order management with state machine
- Monnify payment integration

Built by **Joshe[cyberpriest]**.
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,


    

)
BASE.metadata.create_all(bind=engine)







app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(checkout_router)
app.include_router(payment_router)












