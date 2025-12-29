from fastapi import FastAPI, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Response
from models import Product, CreateProductDTO, UpdateProductDTO
from database import (
    create_tables,
    create_product,
    get_product_by_name,
    get_all_products,
    update_product,
    delete_product,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Ensure DB exists at startup
create_tables()


# ROOT
@app.get("/")
def root():
    return {"message": "API is running"}


# new root for the html page
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


# products table page
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


# product form page to create new product
@app.get("/products-form")
def products_form(request: Request):
    return templates.TemplateResponse(
        "product_form.html",
        {"request": request}
    )


# CREATE (JSON API – Swagger, Postman, etc.)
@app.post("/products", response_model=Product)
def create(dto: CreateProductDTO):
    existing = get_product_by_name(dto.name)
    if existing:
        raise HTTPException(status_code=409, detail="Product already exists")

    return create_product(dto)


# READ ALL
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
def delete(name: str): #defines function that will respond to DELETE requests at the /products/{name} endpoint
    success = delete_product(name) # calls the delete_product function from database
    if not success: # checks if the deletion was unsuccessful
        raise HTTPException(status_code=404, detail="Product not found") # raises 404 error if product not found
    return ""


# new endpoint to create product via form
@app.post("/products-form")
def create_from_form(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    in_stock: bool = Form(False),
):
    # Check how to move business logic to service layer.

    dto = CreateProductDTO(
        name=name,
        price=price,
        in_stock=in_stock
    )

    existing = get_product_by_name(dto.name)
    if existing:
        raise HTTPException(status_code=409, detail="Product already exists")

    new_product = create_product(dto)

    # After creating the product, redirect to the products table page
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "product": new_product
        }
    )