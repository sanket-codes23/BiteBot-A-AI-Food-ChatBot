from fastapi import FastAPI, Request
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services import menu_service
from app.services import cart_service
from app.services import order_service
from app.generic_helper import extract_session_id

app = FastAPI(
    title="Food Ordering Chatbot",
    version="1.0.0"
)


# ==========================================================
# NORMALIZE INTENT NAME
# ==========================================================

def normalize_intent(intent: str) -> str:
    if not intent:
        return ""

    return (
        intent.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


# ==========================================================
# WEBHOOK
# ==========================================================

@app.post("/")
async def webhook(request: Request):

    payload = await request.json()

    query_result = payload.get("queryResult", {})

    intent = normalize_intent(
        query_result.get("intent", {}).get("displayName", "")
    )

    parameters = query_result.get("parameters", {})

    print("Intent:", intent)
    print("Parameters:", parameters)  

    output_contexts = query_result.get("outputContexts", [])

    session_id = ""

    if output_contexts:
        session_id = extract_session_id(
            output_contexts[0]["name"]
        )

    db: Session = SessionLocal()

    try:

        # ================= MENU =================

        if intent == "show menu":
            return menu_service.show_menu(db)

        elif intent == "choose category":
            return menu_service.choose_category(
                parameters,
                db
            )

        # ================= CART =================

        elif intent == "new order":
            return cart_service.start_new_order(
                session_id
            )

        elif intent == "add order":
            return cart_service.add_to_cart(
                parameters,
                session_id,
                db
            )

        elif intent == "show cart":
            return cart_service.show_cart(
                session_id,
                db
            )

        elif intent == "remove order":
            return cart_service.remove_from_cart(
                parameters,
                session_id
            )

        # ================= ORDER =================

        elif intent in ["no more items", "order summary"]:
            return order_service.no_more_items(
                session_id
            )

        elif intent == "order complete":
            return order_service.complete_order(
                session_id,
                db
            )

        elif intent == "track order":
            return order_service.track_order(
                parameters,
                db
            )

        elif intent == "track order id":

            return order_service.track_order(
               parameters,
               db
          )
        

        elif intent == "default welcome intent":

          return {
        "fulfillmentText":
        (
            "👋 Welcome to Food Chatbot!\n\n"
            "I can help you:\n"
            "🍽️ Browse the menu\n"
            "🛒 Place an order\n"
            "📦 Track your order\n"
            "❌ Cancel an order\n\n"
            "Type 'Show Menu' or 'New Order' to get started."
        )
    }
        
        elif intent == "default fallback intent":

           return {
    "fulfillmentText":
    (
        "⚠️ This feature is not available yet.\n\n"
        "Try:\n"
        "• Show Menu\n"
        "• New Order\n"
        "• Show Cart\n"
        "• Track My Order"
    )
}
        
        elif intent == "cancel order id":
           return order_service.cancel_order(
        parameters,
        db
    )
      


        elif intent == "cancel order":
            return order_service.cancel_order(
                parameters,
                db
            )

        # ================= UNKNOWN =================

        return {
            "fulfillmentText":
            f"Intent '{intent}' is not implemented."
        }

    finally:
        db.close()


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/")
def home():
    return {
        "message": "Food Chatbot Backend Running Successfully 🚀"
    }


# ==========================================================
# TEST APIS
# ==========================================================

from app import db_helper


@app.get("/categories")
def categories():

    db = SessionLocal()

    try:
        categories = db_helper.get_all_categories(db)

        return [
            {
                "id": c.category_id,
                "name": c.category_name
            }
            for c in categories
        ]

    finally:
        db.close()


@app.get("/menu/{category}")
def menu(category: str):

    db = SessionLocal()

    try:

        items = db_helper.get_food_items_by_category(
            db,
            category
        )

        return [
            {
                "food": i.food_name,
                "price": float(i.price)
            }
            for i in items
        ]

    finally:
        db.close()


        