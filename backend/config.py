import os
import secrets
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST' , 'localhost')
DB_NAME = os.getenv('DB_NAME' , 'strangercalc')
DB_USER = os.getenv('DB_USER' , 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT' , '5432')

ENABLE_DB = os.getenv("ENABLE_DB", "False").lower() == "true"

# Database URL

DATABASE_URL = None
if ENABLE_DB:
    if not DB_PASSWORD:
        raise ValueError("DB_PASSWORD environment variable not defined (ENABLE_DB=true)!")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Other settings

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    # Keeps the app runnable for local demos without requiring a pre-created .env.
    SECRET_KEY = secrets.token_hex(32)

