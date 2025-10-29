# Flask-quiz-app

# Project Title: Flask-Based Quiz Application with Email Validation
Description:
A dynamic and scalable web-based quiz application built using Flask and MySQL, designed for interactive learning and assessment. The application features secure user authentication, real-time email-based validation for account registration, and a robust MySQL database for managing users, quizzes, and results. It also includes responsive navigation with header, menu, and footer components for an intuitive user experience.

# Key Features:
User Authentication: Secure login, registration, and logout functionalities with password hashing using Werkzeug.

# Email Verification: Automated OTP-based email verification for new user registrations.
Quiz Management: Dynamic quizzes with multiple-choice questions stored in a MySQL database.
Score Tracking: Dedicated score table for tracking user performance across quizzes.
Logging: Integrated logging system for debugging and monitoring application events.
Responsive Design: A clean and responsive user interface with organized navigation.

# Technologies Used:
Backend: Flask, MySQL, Flask-MySQLdb
Frontend: HTML, CSS, Bootstrap (or other frontend frameworks as applicable)
Email Integration: smtplib, MIME for automated email validation
Utilities: Python logging for error tracking and monitoring

# Applications:
E-learning platforms
Online assessments
Knowledge-testing tools for organizations or individuals


Usage on a Resume:
Flask-Based Quiz Application
Developed a scalable web application using Flask and MySQL for online quizzes, featuring secure user authentication, real-time email validation, and dynamic quiz management. Implemented a robust database schema to manage users, quizzes, and scores. Designed and integrated a responsive user interface with organized navigation, enhancing the user experience. Utilized Python logging for application monitoring and error tracking.


conda create -p venv python==3.11 -y 
conda activate venv/

# Create Virtual Environment
python -m venv myvenv
myvenv/Scripts/activate

## Installation dependencies:-
pip install -r requirements.txt

## Run the application 
python -u app.py

## giignore file 
which file contains you do not want to store on the github 

## logging_config 
store application logging configuration

# Example log messages
logging.debug('This is a debug message.')
logging.info('This is an info message.')
logging.warning('This is a warning message.')
logging.error('This is an error message.')
logging.critical('This is a critical message.')

# Explanation of Parameters
filename: Specifies the name of the log file (e.g., app.log).

level: Specifies the log level. Options:

DEBUG: Detailed information, typically for debugging.
INFO: General information about application progress.
WARNING: Indicates something unexpected but still running.
ERROR: A serious problem that might affect the program.
CRITICAL: A severe error that may stop the program.
format: Specifies how the log messages are formatted.


Example: %(asctime)s - %(levelname)s - %(message)s includes:
%(asctime)s: Timestamp of the log.
%(levelname)s: Log level (e.g., DEBUG, INFO).
%(message)s: Log message.
filemode: Determines how the file is opened. Options:

'a' (default): Append to the file.
'w': Overwrite the file.


uvicorn fast-api:app --reload

## React app 

npx create-react-app firstapp
npm start

npm install web-vitals
npm install 

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:jroshan@98@localhost/quiz_app"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

docker build -t welcome-app .


## Docker runs with the following
docker build -t jroshan731/welcome-app .
docker images 


## Run Dockers
docker run -p 5000:5000 welcome-app

## docker port , host
docker psc

## push docker image into docker container
docker login ( jroshan123)

docker image rm -f welcome-app 

# rename 
docker tag jroshan123/welcome-app jroshan123/welcome-app1 


# push 
docker push jroshan123/welcome-app1
docker push jroshan123/welcome-app:lates

docker pull jroshan123/welcome-app1:latest

docker run -d -p 8080:8080 jroshan123/welcome-app1:latest


# 2025 - 10 - 27 
# Backend handline in flask with using mysql

# install Dependencies 
pip install flask mysql-connector-python flask-cors

flask_mysql_app/
│
├── app.py
├── db_config.py
├── requirements.txt
└── .env

📊 7. Test Using curl or Postman
➕ Add Customer

curl -X POST http://127.0.0.1:5000/customers \
-H "Content-Type: application/json" \
-d '{"name":"Alice","email":"alice@example.com","country":"India"}'

📜 Fetch All
curl http://127.0.0.1:5000/customers


🧾 Step 5: Example JSON Requests
Signup
POST /signup
Content-Type: application/json

{
  "username": "roshan",
  "email": "roshan@example.com",
  "password": "mypassword"
}

✅ Response:
{"status": "success", "message": "Signup successful! Please login."}

Login
POST /login
Content-Type: application/json

{
  "username": "roshan",
  "password": "mypassword"
}

✅ Response:
{
  "status": "success",
  "message": "Login successful!",
  "token": "eyJ0eXAiOiJKV1QiLCJh..."
}

Access Protected Dashboard
GET /dashboard
Authorization: Bearer <token>

✅ Response:
{
  "status": "success",
  "message": "Welcome roshan!",
  "data": {
    "user": "roshan",
    "role": "Data Analyst"
  }
}