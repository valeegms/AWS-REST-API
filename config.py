from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}"