import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, '..', 'uploads', 'routines')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}    

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_DEVELOPMENT')
    CORS_ORIGINS = [
        'http://localhost:5173', 
        'http://127.0.0.1:5173'
    ]

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_PRODUCTION')
    CORS_ORIGINS = [
        'http://localhost', 
        'http://10.49.66.30'
    ]