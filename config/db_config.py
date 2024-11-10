import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db_config = {
    'dbname': os.getenv('DB_NAME', 'degreeCompass'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
} 