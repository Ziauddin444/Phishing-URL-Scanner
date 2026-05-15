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

# Environment-specific configurations (DRY: defined via dict instead of classes)
_ENV_CONFIGS = {
    'development': {'DEBUG': True, 'TESTING': False},
    'production': {'DEBUG': False, 'TESTING': False},
    'testing': {'DEBUG': True, 'TESTING': True},
}

def _create_env_config(env_name, overrides):
    """Factory function to create config classes (DRY principle)"""
    class EnvConfig(Config):
        pass
    for key, value in overrides.items():
        setattr(EnvConfig, key, value)
    return EnvConfig

# Create config classes using factory
DevelopmentConfig = _create_env_config('development', _ENV_CONFIGS['development'])
ProductionConfig = _create_env_config('production', _ENV_CONFIGS['production'])
TestingConfig = _create_env_config('testing', _ENV_CONFIGS['testing'])

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig  # SECURITY: Default to production-safe config
}
