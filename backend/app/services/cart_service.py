from fastapi.responses import JSONResponse

from app import db_helper
from app import generic_helper


# ==========================================================
# In-Memory Cart
# ==========================================================

# Stores orders until user confirms.
# Format:
#
# {
#     session_id:{
#          "Pizza":2,
#          "Burger":1
#     }
# }

inprogress_orders = {}


# ==========================================================
# START NEW ORDER
# ==========================================================

def start_new_order(session_id):

    inprogress_orders[session_id] = {}

    return JSONResponse(
        content={
            "fulfillmentText":
            "🍽️ Great! Let's start your order.\n\nType 'Show Menu' to see all available categories."
        }
    )


# ==========================================================
# ADD ITEMS
# ==========================================================

def add_to_cart(
        parameters,
        session_id,
        db
):
    
    

    food_items = parameters.get("food-item")
    quantities = parameters.get("number")

    if not generic_helper.validate_food_list(
            food_items,
            quantities
    ):

        return JSONResponse(
            content={
                "fulfillmentText":
                "Please specify food items and quantities correctly."
            }
        )

    if session_id not in inprogress_orders:

        inprogress_orders[session_id] = {}

    cart = inprogress_orders[session_id]

    invalid_items = []

    for food_name, quantity in zip(
            food_items,
            quantities
    ):

        if not db_helper.food_item_exists(
                db,
                food_name
        ):

            invalid_items.append(food_name)

            continue

        if food_name in cart:

            cart[food_name] += quantity

        else:

            cart[food_name] = quantity

    inprogress_orders[session_id] = cart

    if invalid_items:

        return JSONResponse(
            content={
                "fulfillmentText":
                f"These items are unavailable:\n{', '.join(invalid_items)}"
            }
        )

    order = generic_helper.cart_to_string(cart)

    return JSONResponse(
        content={
            "fulfillmentText":
            f"Added successfully.\n\nCurrent Cart:\n\n{order}\n\nWould you like anything else?"
        }
    )


# ==========================================================
# SHOW CART
# ==========================================================

def show_cart(session_id, db):

    if session_id not in inprogress_orders:
        return JSONResponse(
            content={
                "fulfillmentText": "Your cart is empty."
            }
        )

    cart = inprogress_orders[session_id]

    if not cart:
        return JSONResponse(
            content={
                "fulfillmentText": "Your cart is empty."
            }
        )

    text = "🛒 Your Cart\n\n"

    grand_total = 0

    for item, quantity in cart.items():

        price = db_helper.get_food_price(
            db,
            item
        )

        if price is None:
            continue

        subtotal = price * quantity
        grand_total += subtotal

        text += (
            f"🍽️ {item}\n"
            f"Qty : {quantity}\n"
            f"Price : ₹{price}\n"
            f"Subtotal : ₹{subtotal}\n\n"
        )

    text += "----------------------\n"
    text += f"Grand Total : ₹{grand_total}"

    return JSONResponse(
        content={
            "fulfillmentText": text
        }
    )


# ==========================================================
# REMOVE ITEM
# ==========================================================

def remove_from_cart(
        parameters,
        session_id
):

    if session_id not in inprogress_orders:

        return JSONResponse(
            content={
                "fulfillmentText":
                "Your cart is empty."
            }
        )

    cart = inprogress_orders[session_id]

    food_items = parameters.get("food-item")

    removed = []

    for item in food_items:

        if item in cart:

            del cart[item]

            removed.append(item)

    inprogress_orders[session_id] = cart

    return JSONResponse(
        content={
            "fulfillmentText":
            generic_helper.remove_message(
                removed,
                cart
            )
        }
    )


# ==========================================================
# GET CART
# ==========================================================

def get_cart(
        session_id
):

    return inprogress_orders.get(
        session_id,
        {}
    )


# ==========================================================
# CLEAR CART
# ==========================================================

def clear_cart(
        session_id
):

    if session_id in inprogress_orders:

        del inprogress_orders[session_id]


# ==========================================================
# CART TOTAL ITEMS
# ==========================================================

def cart_item_count(
        session_id
):

    if session_id not in inprogress_orders:

        return 0

    return generic_helper.total_items(
        inprogress_orders[session_id]
    )