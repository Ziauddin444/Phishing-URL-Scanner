"""
Configuration file for Phishing URL Scanner
Stores all app settings and constants
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Model paths
    MODEL_DIR = 'models'
    RANDOM_FOREST_MODEL = os.path.join(MODEL_DIR, 'random_forest_model.joblib')
    SVM_MODEL = os.path.join(MODEL_DIR, 'svm_model.joblib')
    SCALER_MODEL = os.path.join(MODEL_DIR, 'feature_scaler.joblib')
    
    # Data paths
    DATA_DIR = 'data'
    TRAINING_DATA = os.path.join(DATA_DIR, 'training_data.csv')
    
    # Model parameters
    RF_N_ESTIMATORS = 100
    RF_MAX_DEPTH = 20
    SVM_KERNEL = 'rbf'
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    # API settings
    MAX_URL_LENGTH = 2048
    TIMEOUT = 10

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
