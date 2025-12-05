from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# # ---------------- EXAMPLE 1 ----------------
# @app.get("/hello/{username}")
# def say_hello(username: str):
#     return {"message": f"Hello, {username}!"}

# # ---------------- EXAMPLE 2 ----------------
# @app.get("/info")
# def get_info(age: int, country: str):
#     return {
#         "Age received": age,
#         "Country received": country
#     }


# ---------------- EXAMPLE 3 ----------------
class Item(BaseModel):
    price: float
    in_stock: bool

class CreateItemDTO(BaseModel):
    name: str
    price: float
    in_stock: bool


# temp storage (fake db)
items = {}

cola = {"cola": Item(price=1.5, in_stock=True)}
items.update(cola)
pepsi = {"cepsi": Item(price=1.4, in_stock=True)}
items.update(pepsi)

# ------------------- POST -------------------
@app.post("/items")
def create_item(item: CreateItemDTO):
    items.update({item.name: Item(price=item.price, in_stock=item.in_stock)})
    return {
        "message": "Item created successfully",
        "item": item
    }


# ------------------- GET -------------------
@app.get("/items")
def get_items():
    return {
        "total": len(items),
        "items": items
    }


@app.get("/items/{item_name}")
def get_item(item_name: str):
    return items.get(item_name)

# ------------------- PUT -------------------
@app.put("/items/{item_id}")
def update_item(item_name: str, updated_item: Item):

    items[item_name] = updated_item
    items.update({item_name: updated_item})

    return {
        "message": "Item updated!",
        "item": updated_item
    }


# ------------------- DELETE -------------------
@app.delete("/items/{item_id}")
def delete_item(item_name: str):

    print(items)
    deleted = items.pop(item_name)
    return {
        "message": "Item deleted!",
        "deleted": deleted
    }
# To run the app, use the command: uvicorn main:app --reload
#ta modivikoj items per ti aksesau nje item  (cola) me pak fjal nje item specifik
# ta ndroj databasen nvend at tperdori dict
