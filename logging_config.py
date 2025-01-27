import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Example to log when logging is initialized
logging.info("Logging is configured.")


# Configure rotating file handler
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info('This is a log message.')
