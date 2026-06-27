from fastapi.responses import JSONResponse

from app import db_helper
from app import generic_helper


from app.services.cart_service import(
    get_cart,
    clear_cart
)


# ==========================================================
# NO MORE ITEMS
# ==========================================================

def no_more_items(
        session_id
):
    """
    Displays final cart before confirmation.
    """

    cart = get_cart(session_id)

    if not cart:

        return JSONResponse(
            content={
                "fulfillmentText":
                "Your cart is empty."
            }
        )

    return JSONResponse(
        content={
            "fulfillmentText":
            generic_helper.create_order_summary(cart)
        }
    )


# ==========================================================
# COMPLETE ORDER
# ==========================================================

def complete_order(
        session_id,
        db,
        customer_name="Guest"
):
    """
    Places the order.
    """

    cart = get_cart(session_id)

    if not cart:

        return JSONResponse(
            content={
                "fulfillmentText":
                "Your cart is empty."
            }
        )

    order = db_helper.place_complete_order(
        db=db,
        cart=cart,
        customer_name=customer_name
    )

    if order is None:

        return JSONResponse(
            content={
                "fulfillmentText":
                "Sorry! Something went wrong while placing your order."
            }
        )

    clear_cart(session_id)

    return JSONResponse(
        content={
            "fulfillmentText":
            generic_helper.order_success_message(
                order.order_id,
                order.total_price
            )
        }
    )


# ==========================================================
# TRACK ORDER
# ==========================================================


# ==========================================================
# TRACK ORDER
# ==========================================================

def track_order(parameters, db):
    """
    Returns order status.
    """

    print("Track Order Parameters:", parameters)

    order_id = parameters.get("order_id")

    # Handle Dialogflow sending a list
    if isinstance(order_id, list):
        if len(order_id) > 0:
            order_id = order_id[0]
        else:
            order_id = None

    if not order_id:
        return JSONResponse(
            content={
                "fulfillmentText":
                "Please provide your Order ID."
            }
        )

    # Convert to integer
    order_id = int(order_id)

    status = db_helper.get_order_status(
        db,
        order_id
    )

    if status is None:
        return JSONResponse(
            content={
                "fulfillmentText":
                f"No order found with Order ID {order_id}."
            }
        )

    return JSONResponse(
        content={
            "fulfillmentText":
            generic_helper.tracking_message(
                order_id,
                status
            )
        }
    )





# ==========================================================
# CANCEL ORDER
# ==========================================================

def cancel_order(parameters, db):
    """
    Cancels an already placed order.
    """

    order_id = parameters.get("order_id")

    # Handle Dialogflow sending a list
    if isinstance(order_id, list):
        if len(order_id) > 0:
            order_id = order_id[0]
        else:
            order_id = None

    if not order_id:
        return JSONResponse(
            content={
                "fulfillmentText":
                "Please provide the Order ID."
            }
        )

    order_id = int(order_id)

    exists = db_helper.order_exists(
        db,
        order_id
    )

    if not exists:
        return JSONResponse(
            content={
                "fulfillmentText":
                "Order not found."
            }
        )

    success = db_helper.cancel_order(
        db,
        order_id
    )

    if not success:
        return JSONResponse(
            content={
                "fulfillmentText":
                f"Order #{order_id} cannot be cancelled."
            }
        )

    return JSONResponse(
        content={
            "fulfillmentText":
            f"✅ Order #{order_id} has been cancelled successfully."
        }
    )


# ==========================================================
# ORDER DETAILS
# ==========================================================

def order_details(
        parameters,
        db
):
    """
    Shows complete order.
    """

    order_id = parameters.get("order_id")

    if not order_id:

        return JSONResponse(
            content={
                "fulfillmentText":
                "Please provide the Order ID."
            }
        )

    details = db_helper.get_complete_order(
        db,
        int(order_id)
    )

    if details is None:

        return JSONResponse(
            content={
                "fulfillmentText":
                "Order not found."
            }
        )

    text = f"🆔 Order ID: {details['order_id']}\n\n"

    for item in details["items"]:

        text += (
            f"{item['quantity']} x "
            f"{item['food_name']} "
            f"(₹{item['subtotal']})\n"
        )

    text += f"\n💰 Total : ₹{details['total_price']}"

    text += f"\n\n📦 Status : {details['status']}"

    return JSONResponse(
        content={
            "fulfillmentText":
            text
        }
    )