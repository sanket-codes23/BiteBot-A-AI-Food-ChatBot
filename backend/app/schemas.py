from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


# -----------------------------
# Category
# -----------------------------

class CategoryBase(BaseModel):
    category_name: str


class Category(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True


# -----------------------------
# Food Item
# -----------------------------

class FoodItemBase(BaseModel):
    food_name: str
    category_id: int
    price: Decimal
    is_available: bool


class FoodItem(FoodItemBase):
    item_id: int

    class Config:
        from_attributes = True


# -----------------------------
# Order Item
# -----------------------------

class OrderItemBase(BaseModel):
    item_id: int
    quantity: int
    subtotal: Decimal


class OrderItem(OrderItemBase):
    order_item_id: int

    class Config:
        from_attributes = True


# -----------------------------
# Order
# -----------------------------

class OrderBase(BaseModel):
    customer_name: str
    total_price: Decimal


class Order(OrderBase):
    order_id: int
    order_time: datetime

    class Config:
        from_attributes = True


# -----------------------------
# Order Tracking
# -----------------------------

class OrderTracking(BaseModel):
    order_id: int
    status: str

    class Config:
        from_attributes = True