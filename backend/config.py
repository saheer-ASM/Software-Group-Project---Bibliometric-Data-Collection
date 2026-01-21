"""
Configuration settings for the Bibliometric Analysis System
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Database
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'bibliometric_db')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
    
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/bibliometric_data')
    
    # API Keys
    SCOPUS_API_KEY = os.getenv('SCOPUS_API_KEY', '')
    SERP_API_KEY = os.getenv('SERP_API_KEY', '')
    
    # Processing
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', '10'))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '100'))
    
    # Paths
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    EXPORT_DIR = os.path.join(DATA_DIR, 'exports')
    LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
