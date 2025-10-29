from flask import Flask, render_template, request, jsonify, session, redirect, url_for,flash
import mysql.connector
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

import logging
import logging_config  # Automatically sets up logging

from db_config import get_db_connection # Database configuration module

# Main code
logging.info('Application started.')


# app = Flask(__name__)
# CORS(app)
# app.secret_key = "supersecretkey"  # For sessions

# # Database connection
# db = mysql.connector.connect(
#     host="127.0.0.1", # localhost
#     user="root",
#     password="jroshan@98",
#     database="hospital"
# )
# cursor = db.cursor(dictionary=True)

# # ------------------ ROUTES ------------------ #

# @app.route('/')
# def home():
#     if 'user' in session:
#         return redirect(url_for('dashboard'))
#     return render_template('user-login.html')

# @app.route('/user-signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         data = request.get_json()
#         username = data.get('username')
#         email = data.get('email')
#         password = generate_password_hash(data.get('password'))

#         try:
#             cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
#                            (username, email, password))
#             db.commit()
#             return jsonify({"status": "success", "message": "Signup successful! Please login."})
#         except mysql.connector.Error as err:
#             return jsonify({"status": "error", "message": str(err)})

#     return render_template('user-signup.html')

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
#     user = cursor.fetchone()

#     if user and check_password_hash(user['password'], password):
#         session['user'] = user['username']
#         return jsonify({"status": "success", "message": "Login successful!"})
#     else:
#         return jsonify({"status": "error", "message": "Invalid username or password"}), 401

# @app.route('/user-dashboard')
# def dashboard():
#     if 'user' not in session:
#         flash('Please log in to access the dashboard.', 'warning')
#         cursor.close() # closed connection 
#         return redirect(url_for('home'))
        
#     return render_template('user-dashboard.html', username=session['user'])

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     cursor.close() # closed connection
#     return redirect(url_for('home'))

# if __name__ == '__main__':
#     logging.info("Running the main function.")
#     #app.run(debug=True)
#     app.run(debug=True, host='0.0.0.0', port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection

app = Flask(__name__)
CORS(app)

# Database connection
db = mysql.connector.connect(
    host="127.0.0.1", # localhost
    user="root",
    password="jroshan@98",
    database="hospital"
)
cursor = db.cursor(dictionary=True)
# JWT Configuration
app.config["JWT_SECRET_KEY"] = "supersecretkey"  # Change to env var in production
jwt = JWTManager(app)

# ------------------ SIGNUP ------------------ #
@app.route('/user-signup', methods=['POST'])
def signup():
    data = request.get_json()
    username, email, password = data.get('username'), data.get('email'), data.get('password')

    if not all([username, email, password]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    hashed_pw = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_pw))
        conn.commit()
        return jsonify({"status": "success", "message": "Signup successful! Please login."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ------------------ LOGIN ------------------ #
@app.route('/user-login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=user['username'])
        return jsonify({
            "status": "success",
            "message": "Login successful!",
            "token": access_token
        })
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# ------------------ PROTECTED ROUTE ------------------ #
@app.route('/user-dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    return jsonify({
        "status": "success",
        "message": f"Welcome {current_user}!",
        "data": {"user": current_user, "role": "Data Analyst"}
    })

# ------------------ LOGOUT (handled client-side) ------------------ #
@app.route('/')
def home():
    return jsonify({"message": "Flask JWT Auth API is running 🚀"})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
# check_password_hash(stored_password, entered_password)