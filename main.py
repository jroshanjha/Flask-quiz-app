# -------------------
# 6. Main File (main.py)
# -------------------

from blog_api.main import app as blog_app
from ecommerce_api.main import app as ecommerce_app
from ml_api.main import app as ml_app
from chat_api.main import app as chat_app
from todo_api.main import app as todo_app

app = FastAPI(title="FastAPI Project Suite")

app.include_router(blog_app)
app.include_router(ecommerce_app)
app.include_router(ml_app)
app.include_router(chat_app)
app.include_router(todo_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    

# -------------------
# 7. Dockerfile (Dockerfile)
# -------------------

FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
