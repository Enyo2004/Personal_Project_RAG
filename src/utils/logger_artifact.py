## provide the logger 
import logging 
import os 
from pathlib import Path 
from datetime import datetime, UTC
import sys 

# provide the log file 
LOG_FILE = 'logs'

# make the directory 
os.makedirs(LOG_FILE, exist_ok=True)

# provide log format 
LOG_FORMAT = "[Created at: %(asctime)s - Module: %(module)s - Importance: %(levelname)s - Name: %(name)s - Message: %(message)s]"

# provide the full path name 
LOG_PATH = Path(os.path.join(LOG_FILE, f"log_{datetime.now(UTC)}"))


# instantiate the basic config with logging
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)

# provide the logger object 
logger = logging.getLogger()