# Flask-quiz-app


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
