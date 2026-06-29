"""

                    E-COMMERCE  DASHBOARD [PART 1]

                         Overview (top cards)
---------------------------------------------------------------------
Total Revenue  | Total Orders  |  Total Products  |  Total Customers
  ₦450,000     |    120        |     45           |     89
---------------------------------------------------------------------


                       E-COMMERCE  DASHBOARD [PART 1]


                               Orders Section

Recent orders table — customer name, items, total, status (pending/paid/cancelled), date
Order status filter
Click order → see order detail





                                      Products Section

Product list — name, category, price, stock status (available/unavailable)
Quick toggle availability
Add/edit/delete product

"""
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from enums import UserRole


def overview(db: Session, user: models.User):
    total_revenue = db.query(
        func.coalesce(func.sum(models.Order.total), 0)
    ).scalar() or 0.0

    total_orders = db.query(
        func.count(models.Order.id)
    ).scalar() or 0

    total_products = db.query(
        func.count(models.Product.id)
    ).scalar() or 0

    total_customers = db.query(
        func.count(models.User.id)
    ).filter(models.User.role == UserRole.CUSTOMER).scalar() or 0

    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_customers': total_customers
    }


def product_list(db: Session, user: models.User):
    return db.query(models.Product).order_by(models.Product.created_at.desc()).all()