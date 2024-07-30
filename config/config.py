import os
from dotenv import load_dotenv

load_dotenv()

# database
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# telegram
TOKEN = os.environ.get("TOKEN")
PASSWORD_ADMIN = os.environ.get("PASSWORD_ADMIN")
