import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '..', 'database', 'luxury_wheels.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    if not SECRET_KEY:
        raise ValueError("SECRET_KEY não está definida no .env — a app não pode arrancar sem isto.")
