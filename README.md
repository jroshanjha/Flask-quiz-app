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