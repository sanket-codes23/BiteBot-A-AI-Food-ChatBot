import re


# ==========================================================
# SESSION FUNCTIONS
# ==========================================================

def extract_session_id(session_string: str):
    """
    Extracts Dialogflow session id.

    Example:

    projects/project-id/agent/sessions/123456789/contexts/context

    Returns

    123456789
    """

    match = re.search(r"/sessions/(.*?)/contexts", session_string)

    if match:
        return match.group(1)

    return ""


# ==========================================================
# CART FUNCTIONS
# ==========================================================

def cart_to_string(cart: dict):
    """
    Converts

    {
        "Pizza":2,
        "Burger":1
    }

    into

    2 x Pizza
    1 x Burger
    """

    if not cart:
        return "Your cart is empty."

    output = []

    for food_name, quantity in cart.items():

        output.append(
            f"{quantity} x {food_name}"
        )

    return "\n".join(output)


def cart_is_empty(cart: dict):

    return len(cart) == 0


def total_items(cart: dict):

    return sum(cart.values())


# ==========================================================
# RESPONSE FUNCTIONS
# ==========================================================

def menu_categories_to_string(categories):

    if not categories:

        return "No categories available."

    response = "🍽️ Available Categories\n\n"

    for index, category in enumerate(categories, start=1):

        response += f"{index}. {category.category_name}\n"

    return response


def food_items_to_string(food_items):

    if not food_items:

        return "No food items available."

    response = ""

    for item in food_items:

        response += f"• {item.food_name} - ₹{item.price}\n"

    return response


# ==========================================================
# VALIDATION
# ==========================================================

def validate_quantity(quantity):

    if quantity <= 0:

        return False

    return True


def validate_food_list(food_items, quantities):

    if len(food_items) != len(quantities):

        return False

    return True


# ==========================================================
# ORDER SUMMARY
# ==========================================================

def create_order_summary(cart):

    if not cart:

        return "Your cart is empty."

    summary = "🛒 Your Cart\n\n"

    for item, qty in cart.items():

        summary += f"{qty} x {item}\n"

    summary += "\nWould you like to place the order?"

    return summary


# ==========================================================
# SUCCESS MESSAGE
# ==========================================================

def order_success_message(
        order_id,
        total_price
):

    return (

        f"🎉 Your order has been placed successfully!\n\n"

        f"🆔 Order ID: {order_id}\n"

        f"💰 Total Amount: ₹{total_price}\n\n"

        f"You can track your order using the Order ID."

    )


# ==========================================================
# TRACKING MESSAGE
# ==========================================================

def tracking_message(
        order_id,
        status
):

    return (

        f"📦 Order ID: {order_id}\n\n"

        f"Current Status:\n"

        f"{status}"

    )


# ==========================================================
# REMOVE MESSAGE
# ==========================================================

def remove_message(
        removed_items,
        cart
):

    message = ""

    if removed_items:

        message += "Removed:\n"

        for item in removed_items:

            message += f"• {item}\n"

        message += "\n"

    if cart:

        message += "Current Cart\n"

        message += cart_to_string(cart)

    else:

        message += "Your cart is empty."

    return message