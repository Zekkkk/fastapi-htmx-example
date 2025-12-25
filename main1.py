import sqlite3
from pydantic import BaseModel



# DATA MODELS (Pydantic)


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
    price: float
    in_stock: bool


class GetItemDTO(BaseModel):
    name: str



# DATABASE CONNECTION


def get_db_connection():
    conn = sqlite3.connect("items.db")
    conn.row_factory = sqlite3.Row
    return conn



# DATABASE SETUP


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            name TEXT PRIMARY KEY,
            price REAL NOT NULL,
            in_stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def clear_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items")
    conn.commit()
    conn.close()



# DATABASE OPERATIONS (CRUD)


def add_item_to_db(item: CreateItemDTO):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO items (name, price, in_stock)
        VALUES (?, ?, ?)
    """, (item.name, item.price, int(item.in_stock)))

    conn.commit()
    conn.close()


def get_all_items():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    conn.close()

    return [
        DBItem(
            name=row["name"],
            price=row["price"],
            in_stock=bool(row["in_stock"])
        )
        for row in rows
    ]


def get_item_by_name(name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM items WHERE name = ?",
        (name,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return DBItem(
        name=row["name"],
        price=row["price"],
        in_stock=bool(row["in_stock"])
    )



# RUN PROGRAM


create_table()
clear_items()

add_item_to_db(CreateItemDTO(name="Keyboard", price=19.99, in_stock=False))
add_item_to_db(CreateItemDTO(name="Headset", price=20.80, in_stock=True))
add_item_to_db(CreateItemDTO(name="Mouse", price=18.49, in_stock=True))
add_item_to_db(CreateItemDTO(name="Laptop", price=599.99, in_stock=True))

print("All items:")
print(get_all_items())

print("\nSingle items:")
print(get_item_by_name("Keyboard"))
print(get_item_by_name("Headset"))
print(get_item_by_name("Mouse"))
print(get_item_by_name("Laptop"))
print(get_item_by_name("NonExistingItem"))