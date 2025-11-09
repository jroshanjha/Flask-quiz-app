from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from flask_mysqldb import MySQL
#from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
# app.py
import logging
import logging_config  # Automatically sets up logging
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf


# 2025 - 10 - 27

from flask_cors import CORS
from db_config import get_db_connection # Database configuration module
from _db import conn as c# cursor 
from datetime import datetime

# 2025 - 11 - 09 
from db_config import db_conn as db

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# csrf = CSRFProtect(app)

CORS(app)  # Enable Cross-Origin Requests

# Main code
logging.info('Application started.')

# MySQL Configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jroshan@98'
app.config['MYSQL_DB'] = 'quiz_app'

mysql = MySQL(app)

# Utility for sending email verification
otp_store = {}

@app.route('/create_table',methods=['GET', 'POST'])
def create_df():
    cursor = mysql.connect.cursor()
    #cursor.execute('')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100), email VARCHAR(100), password VARCHAR(255))')
    mysql.connection.commit()
    cursor.close()
    return "Table created successfully!"

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        if session['username']=='admin123':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    return render_template('home.html')
    #return render_template('_login.html')

def send_verification_email(email, otp):    
    #https://security.google.com/settings/security/apppasswords
    sender_email = "jroshan731@gmail.com"
    sender_password = "abc@123"
    subject = "Email Verification Code"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject

    body = f"Your verification code is: {otp}"
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) # 465
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.close()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        otp = random.randint(100000, 999999)

        otp_store[email] = otp
        send_verification_email(email, otp)

        flash('A verification code has been sent to your email. Please verify to complete registration.', 'info')
        return redirect(url_for('verify_email', username=username, email=email, password=hashed_password))

    return render_template('register.html')

@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    
    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    # return [username,email,password]

    if request.method == 'POST':
        entered_otp = request.form['otp']
        email = request.form['email']
        # return otp_store
        if email in otp_store and otp_store[email] == int(entered_otp):
            #return otp_store
            #return redirect(url_for('register', username=username, email=email, password=password))
            #return jsonify({"status": "success", "message": "OTP verified successfully!"})
            # cursor = mysql.connection.cursor()
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
                # mysql.connection.commit()
            except Exception as e:
                flash(f"Error inserting user: {e}")
            finally:
                conn.commit()
                cursor.close()

            otp_store.pop(email, None)
            flash('Email verified and registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid verification code. Please try again.', 'danger')

    return render_template('verify_email.html', email=email,otp = otp_store[email])

# 2025 - 10 -27
@app.route('/user-login', methods=['GET'])
def index():
    return render_template('_login.html')

@app.route('/user-login', methods=['POST'])
def user_login():
    data = request.get_json()  # expecting JSON from frontend
    username = data.get('username')
    password = data.get('password')
    # cursor = mysql.connection.cursor()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"status": "success", "message": "Login successful!", "user": user})
    else:
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # `cursor = mysql.connection.cursor()` is creating a cursor object that allows you to interact
        # with the MySQL database connected to your Flask application. This cursor object enables you
        # to execute SQL queries, fetch data, and perform database operations within your Flask
        # routes.
        # cursor = mysql.connection.cursor()
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s ', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            if user['username']=='admin123':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    # cursor = mysql.connection.cursor()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM quizzes')
    quizzes = cursor.fetchall()
    cursor.close()

    return render_template('dashboard.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if 'user_id' not in session:
        flash('Please log in to take the quiz.', 'warning')
        return redirect(url_for('login'))

    # cursor = mysql.connection.cursor()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM questions WHERE quiz_id = %s', (quiz_id,))
    questions = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        score = 0
        total_questions = len(questions)
        data = request.form.to_dict()
        #return jsonify(questions)
        for question in questions:
            selected_option = request.form.get(str(question['id']))
            #return selected_option
            if selected_option == question['correct_option']:
                score += 1

        # cursor = mysql.connection.cursor()
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('INSERT INTO scores (user_id, quiz_id, score,total_questions) VALUES (%s, %s, %s, %s)', (session['user_id'], quiz_id, score,total_questions))
        # mysql.connection.commit()
        conn.commit()
        cursor.close()
        
        flash(f'Your score: {score}/{total_questions} and percentage: {score / total_questions * 100:.2f}%', 'info')
        return redirect(url_for('dashboard')) 
    csrf_token = generate_csrf()
    #return jsonify(csrf_token)   
    #return questions
    return render_template('quiz.html', questions=questions,csrf_token=csrf_token)

# Templates required: base.html, home.html, register.html, verify_email.html, login.html, dashboard.html, quiz.html
# MySQL Tables:
# 1. users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100), email VARCHAR(100), password VARCHAR(255))
# 2. quizzes (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(100))
# 3. questions (id INT AUTO_INCREMENT PRIMARY KEY, quiz_id INT, question_text TEXT, correct_option VARCHAR(100))

# 2025 - 11 - 09 
# ✅ Route: Admin adds a new quiz
@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    try:
        if session['username'] =='admin123':
            conn = db()
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                title = request.form.get('title')
                cursor.execute("INSERT INTO quizzes (title, created_at) VALUES (%s, %s)", (title, datetime.now()))
                conn.commit()
                cursor.close()
                flash('Quiz added successfully!', 'success')
                return redirect(url_for('add_question'))
            return render_template('add_quiz.html')
    except:
        flash('Access denied. Admins only.', 'danger')
        session.clear()
        return redirect(url_for('login'))
    # finally:
    #     cursor.close()
    #     db.close()
    

# ✅ Route: Admin adds questions to a quiz
@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    try:
        # ✅ Ensure only admin can access
        if session.get('username') != 'admin123':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('login'))

        conn = db()
        cursor = conn.cursor(dictionary=True)

        # ✅ Fetch all quizzes for dropdown
        cursor.execute("SELECT id, title FROM quizzes")
        quizzes = cursor.fetchall()

        # ✅ Handle form submission
        if request.method == 'POST':
            quiz_id = request.form.get('quiz_id')
            question_text = request.form.get('question_text')
            option_a = request.form.get('option_a')
            option_b = request.form.get('option_b')
            option_c = request.form.get('option_c')
            option_d = request.form.get('option_d')
            correct_option = request.form.get('correct_option')

            # ✅ Validation (optional but recommended)
            if not (quiz_id and question_text and option_a and option_b and option_c and option_d and correct_option):
                flash('All fields are required.', 'warning')
                return redirect(url_for('add_question'))

            cursor.execute("""
                INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option))
            conn.commit()

            flash('✅ Question added successfully!', 'success')
            return redirect(url_for('add_question'))

        return render_template('add_question.html', quizzes=quizzes)

    except Exception as e:
        print("❌ Error in add_question:", e)
        flash('An error occurred while adding the question.', 'danger')
        return redirect(url_for('login'))

    finally:
        # ✅ Safely close connections
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except:
            pass


# ✅ Route: Show all quizzes and questions
# @app.route('/admin_dashboard')
# def admin_dashboard():
#     #return jsonify({'message': 'Admin Dashboard', 'data': [session['username']]}), 200
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         #return jsonify({'message': 'Admin Dashboard', 'data': [session['username']]}), 200
#         if session['username'] =="admin123": 
#             cursor.execute("""
#                 SELECT q.id AS quiz_id, q.title, que.question_text, que.option_a, que.option_b, que.option_c, que.option_d, que.correct_option
#                 FROM quizzes q
#                 LEFT JOIN questions que ON q.id = que.quiz_id
#                 ORDER BY q.id DESC
#             """)
#             data = cursor.fetchall()
#             #conn.commit()
#             cursor.close()
#             return render_template('admin_dashboard.html', data=data)
#     except:
#         flash('Access denied. Admins only.', 'danger')
#         return redirect(url_for('login'))
#     # finally:
#     #     db.commit()
#     #     cursor.close()

# ✅ Route: Admin dashboard with search
# @app.route('/admin_dashboard')
# def admin_dashboard():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         # return jsonify({'message': 'Admin Dashboard', 'data': [session['username']]}), 200
#         if session['username'] =="admin123": 
#             search_query = request.args.get('search', '').strip()
#             if search_query:
#                 sql = """
#                     SELECT q.id AS quiz_id, q.title, que.question_text, que.option_a, que.option_b, que.option_c, que.option_d, que.correct_option
#                     FROM quizzes q
#                     LEFT JOIN questions que ON q.id = que.quiz_id
#                     WHERE q.title LIKE %s OR que.question_text LIKE %s OR que.option_a LIKE %s OR que.option_b LIKE %s
#                         OR que.option_c LIKE %s OR que.option_d LIKE %s OR que.correct_option LIKE %s
#                     ORDER BY q.id DESC
#                 """
#                 #return jsonify({'message': 'Admin Dashboard 3', 'data': [session['username']]}), 200
#                 like_term = f"%{search_query}%"
#                 cursor.execute(sql, (like_term,)*7)
#             else:
#                 cursor.execute("""
#                     SELECT q.id AS quiz_id, q.title, que.question_text, que.option_a, que.option_b, que.option_c, que.option_d, que.correct_option
#                     FROM quizzes q
#                     LEFT JOIN questions que ON q.id = que.quiz_id
#                     ORDER BY q.id DESC
#                 """)
#             data = cursor.fetchall()
#             cursor.close()
#             #return jsonify({'message': 'Admin Dashboard', 'data': data}), 200
#             return render_template('admin_dashboard.html', records=data, search_query=search_query)
#     except Exception as e:
#         flash(f'Access denied. Admins only. {e}', 'danger')
#         session.clear()
#         return redirect(url_for('login'))

@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    try:
        # ✅ Only allow admin access
        if session.get('username') != 'admin123':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('login'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        search_query = request.args.get('search', '').strip()
        data = []

        # ✅ Search feature
        if search_query:
            sql = """
                SELECT q.id AS quiz_id, q.title, que.question_text, que.option_a, que.option_b, 
                       que.option_c, que.option_d, que.correct_option
                FROM quizzes q
                LEFT JOIN questions que ON q.id = que.quiz_id
                WHERE q.title LIKE %s OR que.question_text LIKE %s OR que.option_a LIKE %s 
                    OR que.option_b LIKE %s OR que.option_c LIKE %s OR que.option_d LIKE %s 
                    OR que.correct_option LIKE %s
                ORDER BY q.id DESC
            """
            like_term = f"%{search_query}%"
            cursor.execute(sql, (like_term,) * 7)
        else:
            cursor.execute("""
                SELECT q.id AS quiz_id, q.title, que.question_text, que.option_a, que.option_b, 
                       que.option_c, que.option_d, que.correct_option,que.id AS id
                FROM quizzes q
                LEFT JOIN questions que ON q.id = que.quiz_id
                ORDER BY q.id DESC
            """)

        data = cursor.fetchall()
        return render_template('admin_dashboard.html', records=data, search_query=search_query)

    except Exception as e:
        print("❌ Error in admin_dashboard:", e)
        flash(f'Error loading admin dashboard. {e}', 'danger')
        return redirect(url_for('login'))

    finally:
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except:
            pass

@app.route('/edit_question/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    try:
        if session.get('username') != 'admin123':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('login'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get question details
        cursor.execute("SELECT * FROM questions WHERE id = %s", (id,))
        question = cursor.fetchone()

        # Get all quizzes for dropdown
        cursor.execute("SELECT id, title FROM quizzes")
        quizzes = cursor.fetchall()

        if not question:
            flash("Question not found!", "warning")
            return redirect(url_for('admin_dashboard'))

        if request.method == 'POST':
            quiz_id = request.form['quiz_id']
            question_text = request.form['question_text']
            option_a = request.form['option_a']
            option_b = request.form['option_b']
            option_c = request.form['option_c']
            option_d = request.form['option_d']
            correct_option = request.form['correct_option']

            cursor.execute("""
                UPDATE questions 
                SET quiz_id=%s, question_text=%s, option_a=%s, option_b=%s, option_c=%s, option_d=%s, correct_option=%s
                WHERE id=%s
            """, (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, id))
            conn.commit()

            flash("Question updated successfully!", "success")
            return redirect(url_for('admin_dashboard'))

        cursor.close()
        return render_template('edit_question.html', question=question, quizzes=quizzes)

    except Exception as e:
        print("Error in edit_question:", e)
        flash(f"Something went wrong!", "danger")
        return redirect(url_for('admin_dashboard'))

@app.route('/delete_question/<int:id>', methods=['GET'])
def delete_question(id):
    try:
        if session.get('username') != 'admin123':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('login'))

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if question exists before deleting
        cursor.execute("SELECT id FROM questions WHERE id = %s", (id,))
        question = cursor.fetchone()

        if not question:
            flash("Question not found!", "warning")
            return redirect(url_for('admin_dashboard'))

        cursor.execute("DELETE FROM questions WHERE id = %s", (id,))
        conn.commit()
        cursor.close()

        flash("Question deleted successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    except Exception as e:
        print("Error in delete_question:", e)
        flash("Something went wrong while deleting.", "danger")
        return redirect(url_for('admin_dashboard'))


# 2025 - 10 - 27 

# ✅ Fetch all records
@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Insert new record
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    country = data.get('country')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customers (name, email, country) VALUES (%s, %s, %s)",
            (name, email, country)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Customer added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Get single record by ID
@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return jsonify(row)
        else:
            return jsonify({'message': 'Customer not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Update record
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    country = data.get('country')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE customers SET name=%s, email=%s, country=%s WHERE id=%s",
            (name, email, country, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Customer updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Delete record
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Customer deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logging.info("Running the main function.")
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
# http://127.0.0.1:5000
