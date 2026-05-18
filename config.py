"""
Configuration file for Phishing URL Scanner
Stores all app settings and constants
Security: Uses environment variables for secrets, never hardcodes production values
"""
import os
from dotenv import load_dotenv
import secrets

load_dotenv()


def _get_secure_secret_key(env):
    """
    SECURITY: Get SECRET_KEY from environment or generate one.
    Production must have SECRET_KEY set in environment.
    
    Args:
        env: Environment name (development, production, testing)
    
    Returns:
        str: SECRET_KEY value
    
    Raises:
        ValueError: If production environment lacks SECRET_KEY
    """
    key = os.environ.get('SECRET_KEY')
    
    if env == 'production':
        if not key:
            raise ValueError(
                'SECURITY ERROR: SECRET_KEY must be set in production environment. '
                'Generate with: python -c "import secrets; print(secrets.token_hex(32))"'
            )
        if len(key) < 32:
            raise ValueError('SECURITY ERROR: SECRET_KEY must be at least 32 characters')
    elif env == 'development':
        # Development only: generate if not set
        key = key or secrets.token_hex(16)
    elif env == 'testing':
        key = key or 'test-secret-key-change-in-production'
    
    return key


class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    # SECURITY: SECRET_KEY set dynamically based on environment
    SECRET_KEY = None
    
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
    
    # Security headers
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

# Environment-specific configurations (DRY: defined via dict instead of classes)
_ENV_CONFIGS = {
    'development': {'DEBUG': True, 'TESTING': False},
    'production': {'DEBUG': False, 'TESTING': False},
    'testing': {'DEBUG': True, 'TESTING': True},
}


def _create_env_config(env_name, overrides):
    """
    Factory function to create config classes (DRY principle).
    Sets SECRET_KEY securely based on environment.
    
    Args:
        env_name: Environment name (development, production, testing)
        overrides: Dictionary of config overrides
    
    Returns:
        EnvConfig: Configuration class for the environment
    
    Raises:
        ValueError: If production environment lacks proper configuration
    """
    class EnvConfig(Config):
        pass
    
    for key, value in overrides.items():
        setattr(EnvConfig, key, value)
    
    # SECURITY: Set SECRET_KEY based on environment
    try:
        EnvConfig.SECRET_KEY = _get_secure_secret_key(env_name)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        if env_name == 'production':
            raise
    
    return EnvConfig

# Create config classes using factory
DevelopmentConfig = _create_env_config('development', _ENV_CONFIGS['development'])
TestingConfig = _create_env_config('testing', _ENV_CONFIGS['testing'])

# Create ProductionConfig with error handling during import
try:
    ProductionConfig = _create_env_config('production', _ENV_CONFIGS['production'])
except ValueError:
    # If production config fails during import, create a placeholder
    # that will fail at app startup (see app.py for enforcement)
    class ProductionConfig(Config):
        DEBUG = False
        TESTING = False
        SECRET_KEY = None  # Will be validated at app startup

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig  # SECURITY: Default to production-safe config
}
