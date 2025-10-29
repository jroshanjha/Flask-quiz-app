# FROM python:3.11-alpine
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# CMD python -u app.py


FROM python:3.11

WORKDIR /project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:project", "--host", "0.0.0.0", "--port", "8000"]


# The Dockerfile snippet you provided is creating a Docker image for a Python application using the `python:3.11-slim` base image. Here's what each instruction does:
# FROM python:3.11-slim
# WORKDIR /app
# COPY . .
# RUN pip install -r requirements.txt
# EXPOSE 5000
# CMD ["python", "app.py"]



# FROM nginx:alpine

# # Set the working directory
# WORKDIR /usr/share/nginx/html

# # Copy dashboard files to Nginx html directory
# COPY . /usr/share/nginx/html

# # Expose port 80
# EXPOSE 80

# # Start Nginx
# CMD ["nginx", "-g", "daemon off;"]


# 🐳 14. Dockerizing Your FastAPI App

# FROM python:3.11
# WORKDIR /app
# COPY . .
# RUN pip install -r requirements.txt
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
