# pip install flask fastai torch

from fastapi import FastAPI,Path,HTTPException
import uvicorn
from flask import *
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

products = {
    1: {"p_id": 1, "name": "Product 1", "price": 10.99,'Year':2025},
    2: {"p_id": 2, "name": "Product 2", "price": 20.99,'Year':2024},
    3: {"p_id": 3,"name": "Product 3", "price": 30.99,'Year':2023},
}
class Product(BaseModel):
    p_id: int
    name: str
    price: float
    Year: int
    
class UpdateProduct(BaseModel):
    p_id: Optional[int] =None
    name: Optional[str] = None
    price: Optional[float] = None
    Year: Optional[int] = None
@app.get("/api/")
def index():
    #return jsonify ({"message": "Hello, World!"})
    return {"message": "Hello, World!"}

@app.get("/api/get-data/{p_id}")
def get_data(p_id: int=Path(...,description="The ID of the product you want to get",gt=0,lt=1000)):
    #return jsonify ({"message": "Hello, World!"})
    product = products.get(p_id)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/api/get-name")
def get_name(name: str): # str=None
    for product in products:
        if products[product]["name"] == name:
            return products[product]
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/api/add-product/{product_id}")
def add_product(product_id: int,product: Product):
    if product_id in products:
        raise HTTPException(status_code=400, detail="Product ID already exists")

    products[product_id] = product.dict()
    return {"message": "Product added successfully"},products[product_id]

@app.put("/api/product-update/{product_id}")
def update_product(product_id: int,product: UpdateProduct):
    if product_id not in products:
        raise HTTPException(status_code=404,detail="Product not found")
    if product.p_id is not None:
        products["p_id"]["product_id"] = product.id
    if product.name is not None:
        products[product_id]["name"] = product.name
    if product.price is not None:
        products[product_id]["price"] = product.price
    if product.Year is not None:
        products[product_id]["Year"] = product.Year
    
    #products[product_id] = product.dict()
    return {"message": "Product updated successfully"},product

@app.delete("/api/product-update/{product_id}")
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404,detail="Product not found")
    del products[product_id]
    return {"message": "Product deleted successfully"},products
     
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


    