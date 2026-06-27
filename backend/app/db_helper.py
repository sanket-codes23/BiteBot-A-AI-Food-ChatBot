from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import (
    Category,
    FoodItem,
    Order,
    OrderItem,
    OrderTracking
)


# ==========================================================
# CATEGORY FUNCTIONS
# ==========================================================

def get_all_categories(db: Session):
    """
    Returns all available food categories.
    """

    return (
        db.query(Category)
        .order_by(Category.category_name)
        .all()
    )


def get_category_by_name(
        db: Session,
        category_name: str
):
    """
    Returns a Category object from category name.
    """

    return (
        db.query(Category)
        .filter(
            func.lower(Category.category_name)
            == category_name.lower()
        )
        .first()
    )


# ==========================================================
# FOOD ITEM FUNCTIONS
# ==========================================================

def get_food_items_by_category(
        db: Session,
        category_name: str
):
    """
    Returns every available food item of a category.
    """

    category = get_category_by_name(
        db,
        category_name
    )

    if not category:
        return []

    return (
        db.query(FoodItem)
        .filter(
            FoodItem.category_id
            == category.category_id
        )
        .filter(
            FoodItem.is_available == True
        )
        .order_by(
            FoodItem.food_name
        )
        .all()
    )


def get_food_item_by_name(
        db: Session,
        food_name: str
):
    """
    Returns a single food item.
    """

    return (
        db.query(FoodItem)
        .filter(
            func.lower(FoodItem.food_name)
            == food_name.lower()
        )
        .first()
    )


def get_food_price(db, food_name):

    food = get_food_item_by_name(db, food_name)

    if not food:
        return None

    return float(food.price)


def food_item_exists(
        db: Session,
        food_name: str
):
    """
    Returns True if food item exists.
    """

    item = get_food_item_by_name(
        db,
        food_name
    )

    return item is not None


def get_food_price(
        db: Session,
        food_name: str
):
    """
    Returns food price.
    """

    item = get_food_item_by_name(
        db,
        food_name
    )

    if item:
        return float(item.price)

    return None


# ==========================================================
# ORDER FUNCTIONS
# ==========================================================

def create_order(
        db: Session,
        customer_name="Guest"
):
    """
    Creates a new order.
    """

    order = Order(
        customer_name=customer_name,
        total_price=0
    )

    db.add(order)

    db.commit()

    db.refresh(order)

    return order


def get_order_by_id(
        db: Session,
        order_id: int
):
    """
    Returns Order object.
    """

    return (
        db.query(Order)
        .filter(
            Order.order_id == order_id
        )
        .first()
    )


def order_exists(
        db: Session,
        order_id: int
):
    """
    Checks if order exists.
    """

    order = get_order_by_id(
        db,
        order_id
    )

    return order is not None


# ==========================================================
# ORDER ITEM FUNCTIONS
# ==========================================================

def add_order_item(
        db: Session,
        order_id: int,
        food_name: str,
        quantity: int
):
    """
    Adds a food item to order.
    """

    food_item = get_food_item_by_name(
        db,
        food_name
    )

    if not food_item:

        return False

    subtotal = float(
        food_item.price
    ) * quantity

    order_item = OrderItem(

        order_id=order_id,

        item_id=food_item.item_id,

        quantity=quantity,

        subtotal=subtotal

    )

    db.add(order_item)

    db.commit()

    return True


def get_order_items(
        db: Session,
        order_id: int
):
    """
    Returns every item of an order.
    """

    return (
        db.query(OrderItem)
        .filter(
            OrderItem.order_id
            == order_id
        )
        .all()
    )


def delete_order_item(
        db: Session,
        order_item_id: int
):
    """
    Deletes one order item.
    """

    item = (
        db.query(OrderItem)
        .filter(
            OrderItem.order_item_id
            == order_item_id
        )
        .first()
    )

    if item:

        db.delete(item)

        db.commit()

        return True

    return False


# ==========================================================
# PRICE FUNCTIONS
# ==========================================================

def calculate_order_total(
        db: Session,
        order_id: int
):
    """
    Calculates order total.
    """

    items = get_order_items(
        db,
        order_id
    )

    total = 0

    for item in items:

        total += float(
            item.subtotal
        )

    return total


def update_order_total(
        db: Session,
        order_id: int
):
    """
    Updates order total.
    """

    order = get_order_by_id(
        db,
        order_id
    )

    if not order:

        return False

    order.total_price = calculate_order_total(
        db,
        order_id
    )

    db.commit()

    return True

# ==========================================================
# ORDER TRACKING FUNCTIONS
# ==========================================================

def create_order_tracking(
        db: Session,
        order_id: int,
        status: str = "Order Received"
):
    """
    Creates tracking entry for an order.
    """

    tracking = OrderTracking(
        order_id=order_id,
        status=status
    )

    db.add(tracking)

    db.commit()

    db.refresh(tracking)

    return tracking


def get_order_tracking(
        db: Session,
        order_id: int
):
    """
    Returns tracking object.
    """

    return (
        db.query(OrderTracking)
        .filter(
            OrderTracking.order_id == order_id
        )
        .first()
    )


def get_order_status(
        db: Session,
        order_id: int
):
    """
    Returns current order status.
    """

    tracking = get_order_tracking(
        db,
        order_id
    )

    if tracking:
        return tracking.status

    return None


def update_order_status(
        db: Session,
        order_id: int,
        status: str
):
    """
    Updates tracking status.
    """

    tracking = get_order_tracking(
        db,
        order_id
    )

    if not tracking:
        return False

    tracking.status = status

    db.commit()

    db.refresh(tracking)

    return True


# ==========================================================
# COMPLETE ORDER FUNCTIONS
# ==========================================================

def place_complete_order(
        db: Session,
        cart: dict,
        customer_name: str = "Guest"
):
    """
    Creates a complete order from cart.

    cart example:
    {
        "Pizza":2,
        "Burger":1
    }
    """

    if len(cart) == 0:
        return None

    order = create_order(
        db,
        customer_name
    )

    for food_name, quantity in cart.items():

        success = add_order_item(
            db,
            order.order_id,
            food_name,
            quantity
        )

        if not success:
            db.rollback()
            return None

    update_order_total(
        db,
        order.order_id
    )

    create_order_tracking(
        db,
        order.order_id,
        "Order Received"
    )

    db.refresh(order)

    return order


# ==========================================================
# ORDER DETAILS
# ==========================================================

def get_complete_order(
        db: Session,
        order_id: int
):
    """
    Returns complete order details.
    """

    order = get_order_by_id(
        db,
        order_id
    )

    if not order:
        return None

    items = []

    order_items = get_order_items(
        db,
        order_id
    )

    for item in order_items:

        food = (
            db.query(FoodItem)
            .filter(
                FoodItem.item_id == item.item_id
            )
            .first()
        )

        items.append({

            "food_name": food.food_name,

            "quantity": item.quantity,

            "price": float(food.price),

            "subtotal": float(item.subtotal)

        })

    return {

        "order_id": order.order_id,

        "customer_name": order.customer_name,

        "order_time": order.order_time,

        "total_price": float(order.total_price),

        "items": items,

        "status": get_order_status(
            db,
            order_id
        )

    }


# ==========================================================
# DELETE ORDER
# ==========================================================

# ==========================================================
# CANCEL ORDER
# ==========================================================

def cancel_order(
        db: Session,
        order_id: int
):
    """
    Marks an order as Cancelled instead of deleting it.
    """

    tracking = get_order_tracking(
        db,
        order_id
    )

    if tracking is None:
        return False

    # If already delivered, don't allow cancellation
    if tracking.status.lower() == "delivered":
        return False

    tracking.status = "Cancelled"

    db.commit()

    db.refresh(tracking)

    return True

# ==========================================================
# DASHBOARD / ADMIN
# ==========================================================

def get_all_orders(
        db: Session
):
    """
    Returns every order.
    """

    return (
        db.query(Order)
        .order_by(
            Order.order_time.desc()
        )
        .all()
    )


def total_orders(
        db: Session
):
    """
    Returns total number of orders.
    """

    return db.query(Order).count()


def total_revenue(
        db: Session
):
    """
    Returns total revenue.
    """

    revenue = (
        db.query(
            func.sum(
                Order.total_price
            )
        )
        .scalar()
    )

    if revenue is None:
        return 0

    return float(revenue)


def available_food_items(
        db: Session
):
    """
    Returns all available food items.
    """

    return (

        db.query(FoodItem)

        .filter(
            FoodItem.is_available == True
        )

        .all()

    )