from fastapi import FastAPI,Depends,HTTPException
import uvicorn
from pydantic import BaseModel 
from fastapi import File, UploadFile

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from fastapi.testclient import TestClient

from fastapi import BackgroundTasks

app = FastAPI()
client = TestClient(app)

# 🧪 11. Testing FastAPI Apps
# Using TestClient from fastapi.testclient
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI"}


#  Middleware and CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Handling cross-origin requests
# Custom middleware hooks

def write_log(msg: str):
    with open("log.txt", "a") as f:
        f.write(msg + "\n")
@app.post("/log/")
def log_message(msg: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, msg)
    return {"message": "Logging in background"}


# Authentication & Authorization
@app.get("/users/me/") # OAuth2 & JWT tokens
def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}

@app.get("/hello")
async def say_hello():
    return {"message": "Hello, World!"}

# Route definitions: @app.get(), @app.post(), etc.
# Auto docs: /docs (Swagger UI), /redoc

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Type annotations for validation
# Optional vs required parameters

#🧾 Request Body & Pydantic Models
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

class File(BaseModel):
    filename: str
    content_type: str
    
# File Uploads
# @app.post("/upload/")
# def upload_file(file: UploadFile = File()):
#     return {"filename": file.filename}

@app.get("/items/")
def create_item(item: Item):
    return item

@app.post("/items/")
def create_item(item: Item):
    return item
# Automatic validation
# Data serialization
# Required and optional fields

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

def verify_token(token: str):
    if token != "valid":
        raise HTTPException(status_code=403, detail="Invalid token")
    return True

# Shared logic injection (e.g., auth, DB sessions
@app.get("/secure-data/")
def secure_data(auth=Depends(verify_token)):
    return {"secure": "data"}


# Response Models & Status Codes
@app.post("/success", status_code=status.HTTP_201_CREATED)
def create_success():
    return JSONResponse(content={"msg": "created"}, status_code=201)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    
# uvicorn main:app --reload