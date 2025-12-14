import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).parent.parent.parent.parent
load_dotenv(basedir / '.env')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    GOOGLE_ADS_YAML_PATH = os.getenv('GOOGLE_ADS_YAML_PATH', 'google-ads.yaml')
    GOOGLE_ADS_CUSTOMER_ID = os.getenv('GOOGLE_ADS_CUSTOMER_ID', '')
