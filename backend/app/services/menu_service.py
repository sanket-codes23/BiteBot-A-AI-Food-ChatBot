from fastapi.responses import JSONResponse

from app import db_helper
from app import generic_helper


# ==========================================================
# SHOW MENU
# ==========================================================

def show_menu(db):
    """
    Returns all available categories.
    """

    categories = db_helper.get_all_categories(db)

    if not categories:
        return JSONResponse(
            content={
                "fulfillmentText":
                "Sorry! Menu is currently unavailable."
            }
        )

    fulfillment_text = (
        "🍽️ Welcome to Food Chatbot\n\n"
        "Please choose a category.\n\n"
    )

    fulfillment_text += generic_helper.menu_categories_to_string(
        categories
    )

    fulfillment_text += "\n\nReply with the category name."

    return JSONResponse(
        content={
            "fulfillmentText": fulfillment_text
        }
    )


# ==========================================================
# CHOOSE CATEGORY
# ==========================================================

def choose_category(parameters, db):
    """
    Displays food items for one or more selected categories.
    """

    categories = parameters.get("menu_category", [])

    if not categories:
        return JSONResponse(
            content={
                "fulfillmentText":
                "Please select a category."
            }
        )

    # Convert a single category into a list
    if not isinstance(categories, list):
        categories = [categories]

    fulfillment_text = ""

    for category in categories:

        category = category.strip()

        food_items = db_helper.get_food_items_by_category(
            db,
            category
        )

        if not food_items:
            fulfillment_text += (
                f"❌ No food items available in {category}.\n\n"
            )
            continue

        fulfillment_text += (
            f"🍴 {category} Menu\n\n"
        )

        fulfillment_text += generic_helper.food_items_to_string(
            food_items
        )

        fulfillment_text += "\n\n"

    fulfillment_text += (
        "Tell me what you would like to order."
    )

    return JSONResponse(
        content={
            "fulfillmentText": fulfillment_text
        }
    )


# ==========================================================
# TODAY'S MENU
# ==========================================================

def todays_menu(db):
    """
    Returns every available food item.
    """

    categories = db_helper.get_all_categories(db)

    if not categories:
        return JSONResponse(
            content={
                "fulfillmentText":
                "Menu unavailable."
            }
        )

    text = "🍽️ Today's Menu\n\n"

    for category in categories:

        text += f"📌 {category.category_name}\n"

        foods = db_helper.get_food_items_by_category(
            db,
            category.category_name
        )

        for food in foods:

            text += (
                f"• {food.food_name} - ₹{food.price}\n"
            )

        text += "\n"

    return JSONResponse(
        content={
            "fulfillmentText": text
        }
    )