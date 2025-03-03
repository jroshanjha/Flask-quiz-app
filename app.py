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

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    return render_template('home.html')

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

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if email in otp_store and otp_store[email] == int(entered_otp):
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            cursor.close()

            otp_store.pop(email, None)
            flash('Email verified and registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid verification code. Please try again.', 'danger')

    return render_template('verify_email.html', email=email,otp = otp_store[email])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s ', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
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

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM quizzes')
    quizzes = cursor.fetchall()
    cursor.close()

    return render_template('dashboard.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if 'user_id' not in session:
        flash('Please log in to take the quiz.', 'warning')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM questions WHERE quiz_id = %s', (quiz_id,))
    questions = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        score = 0
        total_questions = len(questions)
        # return jsonify(request)
        for question in questions:
            selected_option = request.form.get(str(question[0]))
            if selected_option == question[-1]:
                score += 1

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO scores (user_id, quiz_id, score,total_questions) VALUES (%s, %s, %s, %s)', (session['user_id'], quiz_id, score,total_questions))
        mysql.connection.commit()
        cursor.close()
        
        flash(f'Your score: {score}/{total_questions} and percentage: {score / total_questions * 100:.2f}%', 'info')
        return redirect(url_for('dashboard'))    

    return render_template('quiz.html', questions=questions)

# Templates required: base.html, home.html, register.html, verify_email.html, login.html, dashboard.html, quiz.html
# MySQL Tables:
# 1. users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100), email VARCHAR(100), password VARCHAR(255))
# 2. quizzes (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(100))
# 3. questions (id INT AUTO_INCREMENT PRIMARY KEY, quiz_id INT, question_text TEXT, correct_option VARCHAR(100))

if __name__ == '__main__':
    logging.info("Running the main function.")
    app.run(debug=True)
# http://127.0.0.1:5000