import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "jroshan@98"),
        database=os.getenv("MYSQL_DB", "quiz_app")
    )
    return connection

def db_conn():
  # ✅ MySQL connection
  # 
  db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jroshan@98",  # your MySQL password
    database="quiz_app"  # your database name
)
  return db

# Created _at_ 2025 - 10 - 27
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(200),
        email VARCHAR(200),
        country VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()

# create_users_table()


def close_db_connection(connection):
    if connection.is_connected():
        connection.close()
        
def create_orders_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        amount DECIMAL(10, 2),
        FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_orders_table()

# -------------------
# 1. Blogging Platform API (project.py)
# -------------------
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional    

# app = FastAPI(title="Blogging Platform API")    

def create_blog_posts_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists blog_posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        content TEXT,
        author VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_blog_posts_table()
# -------------------
# 2. E-commerce Backend API (project.py)
# -------------------

def create_products_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        price DECIMAL(10, 2),
        in_stock BOOLEAN,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_products_table()
# -------------------
# 3. Social Media Platform API (project.py)   
# -------------------
def create_users_table_social_media():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists sm_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        email VARCHAR(100),
        password VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_users_table_social_media()
def create_posts_table_social_media():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists sm_posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES sm_users(id)
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()    
    
# create_posts_table_social_media()

# -------------------
# 4. ML Model Scoring API (project.py)
# -------------------
def create_model_requests_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists model_requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        input_data TEXT,
        prediction_result TEXT,
        requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_model_requests_table()
# -------------------
# 5. Chat API (project.py)
# -------------------
def create_chats_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists chats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES sm_users(id)
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
# create_chats_table()
# -------------------
# 6. Quiz Application API (project.py)
# -------------------
def create_quiz_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE if not exists quizzes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100)
        )
      ''')
    
    cursor.execute('''
        CREATE TABLE if not exists questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        quiz_id INT,
        question_text TEXT,
        correct_option VARCHAR(100),
        FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )
      ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    
# create_quiz_tables()
# -------------------
# 7. Payment Gateway API (project.py)   
# -------------------

def create_payments_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists payments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        amount DECIMAL(10, 2),
        status VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES sm_users(id)
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_payments_table()
# -------------------
# 8. Task Management API (project.py)
# -------------------

def create_tasks_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        description VARCHAR(255),
        is_done BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_tasks_table()
# -------------------
# 9. Inventory Management API (project.py)   
# -------------------   
def create_inventory_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists inventory (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(255),
        quantity INT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_inventory_table()
# -------------------
# 10. To-Do App API (project.py)   
# -------------------
def create_todo_tasks_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists todo_tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        description VARCHAR(255),
        is_done BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_todo_tasks_table()
# -------------------
# 3. ML Model Scoring API (ml_model_api/main.py)
# -------------------   
def create_ml_model_requests_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists ml_model_requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        input_data TEXT,
        prediction_result TEXT,
        requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_ml_model_requests_table()
# -------------------
# 4. Chat API (chat_api/main.py)
# -------------------
def create_chats_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists chat_messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES sm_users(id)
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()
    
# create_chats_table()
# -------------------   
# 5. To-Do App API (todo_api/main.py)
# -------------------
def create_todo_tasks_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE if not exists todo_app_tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        description VARCHAR(255),
        is_done BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
      ''')
    conn.commit()
    cursor.close()
    conn.close()


def create_all_tables():
    create_users_table()
    create_orders_table()
    create_blog_posts_table()
    create_products_table()
    create_users_table_social_media()
    create_posts_table_social_media()
    create_model_requests_table()
    create_chats_table()
    create_quiz_tables()
    create_payments_table()
    create_tasks_table()
    create_inventory_table()
    create_todo_tasks_table()
    create_ml_model_requests_table()
    create_chats_table()
    create_todo_tasks_table()
# create_all_tables()

def drop_all_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    tables = [
        "customers", "orders", "blog_posts", "products", "sm_users",
        "sm_posts", "model_requests", "chats", "quizzes", "questions",
        "payments", "tasks", "inventory", "todo_tasks",
        "ml_model_requests", "chat_messages", "todo_app_tasks"
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()
    cursor.close()
    conn.close()
    
# drop_all_tables()


#table 
def table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""  
                   CREATE TABLE if not exists users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                     email VARCHAR(100) NOT NULL UNIQUE,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(100) NOT NULL
                )
                  """)
    cursor.execute(f"""
                   INSERT INTO users (username,email, password)
                   VALUES ('jroshan123','jroshan@gmail.com', 'jroshan@98'), ('jroshancode98','jroshancode@gmail.com','jroshancode@98');
                   
                   """)
    conn.commit()
    # rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return True

# table()