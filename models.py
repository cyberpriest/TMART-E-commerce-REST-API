from database import BASE
from enums import OrderStatus, UserRole, UserStatus
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, Boolean, String, DateTime, ForeignKey, Float, Enum as SQLAEnum,event
from datetime import datetime, UTC
from slugify import slugify



class User(BASE):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_pw: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLAEnum(UserRole, name='user_role'), default=UserRole.CUSTOMER, nullable=False)
    status: Mapped[UserStatus] = mapped_column(SQLAEnum(UserStatus, name='user_status'), default=UserStatus.ACTIVE, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=UTC))
    carts: Mapped[list['Cart']] = relationship('Cart', back_populates='owner')
    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')


class Category(BASE):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=UTC))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')
@event.listens_for(Category, 'before_insert')
def generate_slug(mapper, connection, target):
    target.slug = slugify(target.name)  # target is basically self here


class Product(BASE):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=UTC))
    category: Mapped['Category'] = relationship('Category', back_populates='products')
    cart_items: Mapped[list['CartItems']] = relationship('CartItems', back_populates='product')


class Cart(BASE):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    is_checked_out: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=UTC))
    owner: Mapped['User'] = relationship('User', back_populates='carts')
    items: Mapped[list['CartItems']] = relationship('CartItems', back_populates='cart',cascade='all, delete-orphan')


class CartItems(BASE):
    __tablename__ = 'cart_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey('carts.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=UTC))
    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')
    product: Mapped['Product'] = relationship('Product', back_populates='cart_items')


class Order(BASE):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SQLAEnum(OrderStatus, name='order_status'), default=OrderStatus.PENDING, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=UTC))
    user: Mapped['User'] = relationship('User', back_populates='orders')
    items: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='order',cascade='all, delete-orphan')


class OrderItem(BASE):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    order: Mapped['Order'] = relationship('Order', back_populates='items')
    product: Mapped['Product'] = relationship('Product')