"""
Application Configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
basedir = Path(__file__).parent.parent.parent.parent
load_dotenv(basedir / '.env')


class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 
        'postgresql://postgres:postgres@localhost:5432/pathik_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # Google Ads API
    GOOGLE_ADS_YAML_PATH = os.getenv('GOOGLE_ADS_YAML_PATH', 'google-ads.yaml')
    
    # CORS
    CORS_HEADERS = 'Content-Type'
