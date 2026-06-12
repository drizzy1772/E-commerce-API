


from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.models import OrderStatus

class Product(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    is_active: bool
    category_id: int
    
class ProductCreate(Product):
    pass

class ProductResponse(Product):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Category(BaseModel):
    name: str
    slug: str

class CategoryCreate(Category):
    pass

class CategoryResponse(Category):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CartItem(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItem):
    pass

class CartResponse(CartItem):
    id: int
    cart_id: int
    model_config = ConfigDict(from_attributes=True)


class Order(BaseModel):
    user_id: int
    total_amount: float
    
class OrderCreate(Order):
    pass

class OrderResponse(Order):
    id: int
    status: OrderStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class VerifyRequest(BaseModel):
    email: str
    code: str

class ForgotPassword(BaseModel):
    email: str

class ResetPassword(BaseModel):
    email: str
    code: str
    new_password: str







