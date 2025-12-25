from pydantic import BaseModel
#what does a product contain
class Product(BaseModel):
    name: str
    price: float
    in_stock: bool


#what do i require from the client to create a product
class CreateProductDTO(BaseModel):
    name: str
    price: float
    in_stock: bool


#when updated the name doesn't usually change only price and stock
class UpdateProductDTO(BaseModel):
    price: float
    in_stock: bool

