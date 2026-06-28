




from typing import Optional
from sqlalchemy import Integer, String, ForeignKey, Enum, Column, Float, Boolean, Numeric, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import DateTime
from datetime import datetime, timedelta, timezone
import enum

class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "category"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)
    products: Mapped[list["Product"]] = relationship(back_populates="category")
    
class Product(Base):
    __tablename__ = "product"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    stock: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="products")
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product")
    
class Cart(Base):
    __tablename__ = "cart"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    items: Mapped[list["CartItem"]] = relationship(back_populates="cart")
    
class CartItem(Base):
    __tablename__ = "cartitem"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"))
    cart: Mapped["Cart"] = relationship(back_populates="items")
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped["Product"] = relationship(back_populates="cart_items")
    

class OrderStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")

class OrderItem(Base):
    __tablename__ = "orderitem"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int]  = mapped_column(ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    quantity: Mapped[int]
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2))
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
    

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    verification_code: Mapped[Optional[str]] = mapped_column(nullable=True)
    reset_code: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    role: Mapped[UserRole ]= mapped_column(Enum(UserRole), default=UserRole.USER)


    
        
class RefreshToken(Base):
    __tablename__ = "refreshtoken"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=7)
    )
    is_revoked: Mapped[bool] = mapped_column(default=False)
    