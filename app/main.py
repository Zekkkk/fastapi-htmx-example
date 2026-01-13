from fastapi import FastAPI, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request

from .models import Product, CreateProductDTO, UpdateProductDTO
from .database import (
    create_tables,
    create_product,
    get_product_by_name,
    get_all_products,
    update_product,
    delete_product,
)

app = FastAPI()

# IMPORTANT: templates folder location
templates = Jinja2Templates(directory="app/templates")

# Ensure DB exists at startup
create_tables()


# ROOT
@app.get("/")
def root():
    return {"message": "API is running"}


# HTML PAGE
@app.get("/products-page")
def products_page(request: Request):
    products = get_all_products()
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": products
        }
    )


# PRODUCTS TABLE (HTMX)
@app.get("/products-table")
def products_table(request: Request):
    products = get_all_products()
    return templates.TemplateResponse(
        "products_table.html",
        {
            "request": request,
            "products": products
        }
    )


# PRODUCT FORM (HTMX)
@app.get("/products-form")
def products_form(request: Request):
    return templates.TemplateResponse(
        "product_form.html",
        {"request": request}
    )


# CREATE (JSON API)
@app.post("/products", response_model=Product)
def create(dto: CreateProductDTO):
    existing = get_product_by_name(dto.name)
    if existing:
        raise HTTPException(status_code=409, detail="Product already exists")

    return create_product(dto)


# READ ALL (JSON)
@app.get("/products", response_model=list[Product])
def read_all():
    return get_all_products()


# READ ONE
@app.get("/products/{name}", response_model=Product)
def read_one(name: str):
    product = get_product_by_name(name)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# UPDATE
@app.put("/products/{name}", response_model=Product)
def update(name: str, dto: UpdateProductDTO):
    product = update_product(name, dto)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# DELETE
@app.delete("/products/{name}")
def delete(name: str):
    success = delete_product(name)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return ""


# CREATE VIA FORM (HTMX)
@app.post("/products-form")
def create_from_form(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    in_stock: bool = Form(False),
):
    dto = CreateProductDTO(
        name=name,
        price=price,
        in_stock=in_stock
    )

    existing = get_product_by_name(dto.name)
    if existing:
        raise HTTPException(status_code=409, detail="Product already exists")

    create_product(dto)

    return templates.TemplateResponse(
        "products_table.html",
        {
            "request": request,
            "products": get_all_products()
        }
    )
