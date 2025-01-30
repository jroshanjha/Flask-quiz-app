# pip install flask fastai torch

from fastapi import FastAPI,Path,HTTPException,Depends,Request

import uvicorn
# from flask import *
from pydantic import BaseModel
from typing import Optional,Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId
import os

import logging
import logging_config

app = FastAPI()
security = HTTPBasic()

# Main code
logging.info('Application started.')

# Configure Jinja2 template directory
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    
# MongoDB connection
MONGO_URI = "mongodb://localhost:27017"  # Replace with your MongoDB URI
client = MongoClient(MONGO_URI)
db = client["my-db"]  # Database name
collection = db["employees"]  # Collection name

@app.get("/api/")
def index():
    #return jsonify ({"message": "Hello, World!"})
    return {"message": "Hello, World!"}
    
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    #fetch = collection.find_one() # find_one({})
    fetch = collection.find_one({"_id":ObjectId(id)})
    if fetch is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse(
        "item.html", {"request": request, "id": id, "fetch": fetch}
    )
    
@app.get("/api/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}

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


    