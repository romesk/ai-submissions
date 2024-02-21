import os
from dotenv import load_dotenv


load_dotenv('.env')

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
