from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "price": 24.99, "stock": 50},
    {"id": 2, "name": "Wireless Keyboard", "price": 34.99, "stock": 50},
    {"id": 3, "name": "USB Cable", "price": 9.99, "stock": 100}
]

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, description="Product name cannot be empty")
    price: float = Field(gt=0, description="Price must be greater than 0")
    stock: int = Field(ge=0, default=0, description="Stock cannot be negative")

@app.get("/")
def home():
    return {"message":"Welcome to the E-commerce API!"}

@app.get("/products")
def get_products():
    return PRODUCTS

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id {product_id} was not found"
    )

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate):
    next_id = max(product["id"] for product in PRODUCTS) + 1
    new_product = {
        "id": next_id,
        "name": payload.name,
        "price": payload.price,
        "stock": payload.stock
    }
    PRODUCTS.append(new_product)
    return new_product
