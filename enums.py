from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'admin'
    CUSTOMER = 'customer'
    STAFF = 'staff'


class UserStatus(str, Enum):
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    DEACTIVATED = 'deactivated'


class OrderStatus(str, Enum):
    PENDING = 'pending'
    PAID = 'paid'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    RETURNED = 'returned'