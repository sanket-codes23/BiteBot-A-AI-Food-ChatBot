from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    text
)

from sqlalchemy.orm import relationship

from app.database import Base


# ==========================
# Categories Table
# ==========================

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), unique=True, nullable=False)

    food_items = relationship("FoodItem", back_populates="category")


# ==========================
# Food Items Table
# ==========================

class FoodItem(Base):
    __tablename__ = "food_items"

    item_id = Column(Integer, primary_key=True, index=True)

    food_name = Column(String(100), unique=True, nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=False
    )

    price = Column(DECIMAL(10, 2), nullable=False)

    is_available = Column(Boolean, default=True)

    category = relationship("Category", back_populates="food_items")

    order_items = relationship("OrderItem", back_populates="food_item")


# ==========================
# Orders Table
# ==========================

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(100))

    order_time = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    total_price = Column(
        DECIMAL(10, 2),
        default=0
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete"
    )

    tracking = relationship(
        "OrderTracking",
        uselist=False,
        back_populates="order",
        cascade="all, delete"
    )


# ==========================
# Order Items Table
# ==========================

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id")
    )

    item_id = Column(
        Integer,
        ForeignKey("food_items.item_id")
    )

    quantity = Column(Integer, nullable=False)

    subtotal = Column(
        DECIMAL(10, 2),
        nullable=False
    )

    order = relationship(
        "Order",
        back_populates="items"
    )

    food_item = relationship(
        "FoodItem",
        back_populates="order_items"
    )


# ==========================
# Order Tracking Table
# ==========================

class OrderTracking(Base):
    __tablename__ = "order_tracking"

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        primary_key=True
    )

    status = Column(
        String(50),
        nullable=False
    )

    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP")
    )

    order = relationship(
        "Order",
        back_populates="tracking"
    )