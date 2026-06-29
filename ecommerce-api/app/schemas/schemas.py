


from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.models import OrderStatus
from pydantic import BaseModel, field_validator, ValidationError, EmailStr
from pydantic_core import PydanticCustomError

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
    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be at least 1")
        return v
    

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
    email: EmailStr
    password: str
    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        errors = []

        if len(value) < 8:
            errors.append('at least 8 characters')
        if not any(c.isupper() for c in value):
            errors.append("one uppercase letter should be")
        if not any(c.isdigit() for c in value):
            errors.append("one digit")
        if errors:
            raise ValueError(', '.join(errors))
        return value

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
    email: EmailStr
    code: str
    
class ForgotPassword(BaseModel):
    email: EmailStr
        
class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        errors = []

        if len(value) < 8:
            errors.append('at least 8 characters')
        if not any(c.isupper() for c in value):
            errors.append("one uppercase letter should be")
        if not any(c.isdigit() for c in value):
            errors.append("one digit")
        if errors:
            raise ValueError(', '.join(errors))
        return value
