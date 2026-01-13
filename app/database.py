import sqlite3
from .models import Product, CreateProductDTO, UpdateProductDTO




# DB connection

def get_db_connection():
    conn = sqlite3.connect("products.db")
    conn.row_factory = sqlite3.Row
    return conn



# DB setup

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            in_stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()



# CREATE

def create_product(dto: CreateProductDTO) -> Product:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, in_stock) VALUES (?, ?, ?)",
        (dto.name, dto.price, int(dto.in_stock))
    )

    conn.commit()
    conn.close()

    return Product(
        name=dto.name,
        price=dto.price,
        in_stock=dto.in_stock
    )



# READ ONE

def get_product_by_name(name: str) -> Product | None:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, price, in_stock FROM products WHERE name = ?",
        (name,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return Product(
        name=row["name"],
        price=row["price"],
        in_stock=bool(row["in_stock"])
    )



# READ ALL

def get_all_products() -> list[Product]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, price, in_stock FROM products")
    rows = cursor.fetchall()
    conn.close()

    return [
        Product(
            name=row["name"],
            price=row["price"],
            in_stock=bool(row["in_stock"])
        )
        for row in rows
    ]



# UPDATE

def update_product(name: str, dto: UpdateProductDTO) -> Product | None:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE products SET price = ?, in_stock = ? WHERE name = ?",
        (dto.price, int(dto.in_stock), name)
    )

    if cursor.rowcount == 0:
        conn.close()
        return None

    conn.commit()
    conn.close()

    return Product(
        name=name,
        price=dto.price,
        in_stock=dto.in_stock
    )



# DELETE

def delete_product(name: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE name = ?",
        (name,)
    )

    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return deleted