# from flask_mysqldb import MySQL
import mysql.connector
from flask_mysqldb import MySQL

# Database Initialization
# MySQL Connection Configuration
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jroshan@98",
    #database="quiz_app"
)
cursor = conn.cursor()

# Creating a new database or Table
#cursor.execute("CREATE DATABASE IF NOT EXISTS quiz_app")
#print("Database 'learning_model' created successfully!")

# create Uers table

def user_table():
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_app.users (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                username VARCHAR(100) NOT NULL, 
                email VARCHAR(100) NOT NULL UNIQUE, 
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.commit()
        conn.close()
        print("Table 'users' created successfully!")
#user_table() 

def quiz_table():
    cursor= conn.cursor()
    try:
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS quiz_app.quizzes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )                   
                    """)
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.commit()
        print("Table 'quizzes' created successfully!")   
#quiz_table()
def questions_table():
    cursor= conn.cursor()
    try:
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS quiz_app.questions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        quiz_id INT NOT NULL,
                        question_text TEXT NOT NULL,
                        option_a VARCHAR(255) NOT NULL,
                        option_b VARCHAR(255) NOT NULL,
                        option_c VARCHAR(255) NOT NULL,
                        option_d VARCHAR(255) NOT NULL,
                        correct_option ENUM('A', 'B', 'C', 'D') NOT NULL,
                        FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE ON UPDATE CASCADE
                    )
                    """)
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.commit()
        # conn.close()
        print("Table 'questions' created successfully!")
#questions_table()

def dummy_data():
    cursor = conn.cursor()
    try:
        
        cursor.execute("""
                        INSERT INTO quiz_app.quizzes (title) VALUES
                        ('General Knowledge Quiz'),
                        ('Science Quiz'),
                        ('History Quiz'),
                        ('Programming Basics Quiz')
                    """)
        cursor.execute("""
                    INSERT INTO quiz_app.questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option) VALUES
                        -- General Knowledge Quiz
                        (1, 'What is the capital of France?', 'Berlin', 'Madrid', 'Paris', 'Rome', 'C'),
                        (1, 'Who wrote "Romeo and Juliet"?', 'Charles Dickens', 'William Shakespeare', 'Mark Twain', 'Ernest Hemingway', 'B'),
                        (1, 'What is the largest planet in our solar system?', 'Earth', 'Jupiter', 'Mars', 'Saturn', 'B'),

                        -- Science Quiz
                        (2, 'What is the chemical symbol for water?', 'H2O', 'O2', 'CO2', 'HO', 'A'),
                        (2, 'What is the speed of light?', '300,000 km/s', '150,000 km/s', '450,000 km/s', '200,000 km/s', 'A'),
                        (2, 'What is the powerhouse of the cell?', 'Nucleus', 'Mitochondria', 'Ribosome', 'Cytoplasm', 'B'),

                        -- History Quiz
                        (3, 'Who was the first President of the United States?', 'Abraham Lincoln', 'George Washington', 'Thomas Jefferson', 'John Adams', 'B'),
                        (3, 'In what year did World War II end?', '1942', '1945', '1948', '1950', 'B'),
                        (3, 'Who discovered America?', 'Christopher Columbus', 'Marco Polo', 'Leif Erikson', 'Vasco da Gama', 'A'),

                        -- Programming Basics Quiz
                        (4, 'What does HTML stand for?', 'HyperText Markup Language', 'Home Tool Markup Language', 'Hyperlink Text Markup Language', 'Hyperlink Markup Language', 'A'),
                        (4, 'Which language is used for web development?', 'Python', 'JavaScript', 'C++', 'SQL', 'B'),
                        (4, 'What does CSS stand for?', 'Cascading Style Sheets', 'Creative Style Sheets', 'Computer Style Sheets', 'Colorful Style Sheets', 'A');

                    """)
    except Exception as e:
        print(f"Error inserting dummy data: {e}")
    finally:
        conn.commit()
        print("Dummy data inserted successfully!")
#dummy_data()

def score_table():
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_app.scores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            quiz_id INT NOT NULL,
            score INT NOT NULL,
            total_questions INT NOT NULL,
            percentage DECIMAL(5, 2) AS (score / total_questions * 100) STORED,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
        )

        """)
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.commit()
        # conn.close()
        print("Table 'scores' created successfully!")
score_table()
conn.close()
    



