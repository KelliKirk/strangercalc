import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST' , 'localhost')
DB_NAME = os.getenv('DB_NAME' , 'strangercalc')
DB_USER = os.getenv('DB_USER' , 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT' , '5432')

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD environment variable not defined!")

# Database URL

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Other settings

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not defined!")

