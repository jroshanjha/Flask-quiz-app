# FastAPI Project Suite
# Includes: Blog API, E-commerce Backend, ML Model Scoring API, Chat API, and To-Do App API

# We'll scaffold each project in a modular format. Let's begin with basic structure and one main file per app.

# -------------------
# 1. Blog API (blog_api/main.py)
# -------------------

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Blog API")

class BlogPost(BaseModel):
    id: int
    title: str
    content: str
    author: str

posts = []

@app.post("/posts/", response_model=BlogPost)
def create_post(post: BlogPost):
    posts.append(post)
    return post

@app.get("/posts/", response_model=List[BlogPost])
def get_posts():
    return posts

# -------------------
# 2. E-commerce Backend (ecommerce_api/main.py)
# -------------------

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="E-commerce API")

class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

products = []

@app.post("/products/", response_model=Product)
def add_product(product: Product):
    products.append(product)
    return product

@app.get("/products/")
def list_products():
    return products

# -------------------
# 3. ML Model Scoring API (ml_api/main.py)
# -------------------

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ML Model Scoring API")

class Features(BaseModel):
    f1: float
    f2: float
    f3: float

model = joblib.load("model.pkl")  # Pre-trained model file

@app.post("/predict")
def predict(features: Features):
    data = [[features.f1, features.f2, features.f3]]
    prediction = model.predict(data)
    return {"prediction": prediction.tolist()}

# -------------------
# 4. Chat API (chat_api/main.py)
# -------------------

from fastapi import FastAPI, WebSocket

app = FastAPI(title="Chat API")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

# -------------------
# 5. To-Do App API (todo_api/main.py)
# -------------------

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="To-Do App API")

class Task(BaseModel):
    id: int
    description: str
    is_done: bool = False

tasks = []

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def list_tasks():
    return tasks
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
