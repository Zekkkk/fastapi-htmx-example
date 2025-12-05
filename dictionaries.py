from pydantic import BaseModel

class Item(BaseModel):
    price: float
    in_stock: bool

class DBItem(Item):
    name: str

class CreateItemDTO(BaseModel):
    name: str
    price: float
    in_stock: bool

class UpdateItemDTO(BaseModel):
    name: str
    price: float
    in_stock: bool

class GetItemDTO(BaseModel):
    name: str

items = {}

def add_item_to_db(item: DBItem):
    items[item.name] = Item(price=item.price, in_stock=item.in_stock)

def get_all_items():
    return items

def get_item_by_name(name: str):
    return items.get(name)

item = Item(price=19.99, in_stock=True)
db_item = DBItem(name="Sample Item", price=18.99, in_stock=True)
item_dto = CreateItemDTO(name="DTO Item", price=17.99, in_stock=True)

print(item)
print(db_item)
print(item_dto)

print("Database:")

print(get_all_items())

add_item_to_db(DBItem(name="Another Item", price=15.99, in_stock=False))

print(get_all_items())

add_item_to_db(DBItem(name="Yet Another Item", price=16.99, in_stock=False))

print(get_all_items())

print(get_item_by_name("Sample Item"))

print(get_item_by_name("Another Item"))
