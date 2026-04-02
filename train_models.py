"""
Training Script - Generate sample data and train models
Run this script to train the phishing detection models
"""
import sys
sys.path.insert(0, '/Users/ziauddin/Phishing URL Scanner')

from src.model_trainer import ModelTrainer
from config import Config

# Sample phishing URLs (for demonstration)
SAMPLE_PHISHING_URLS = [
    'http://194.62.25.1/bank.com.php',
    'http://10.0.0.1/paypal-login.html',
    'https://am4zon.com/account/login',
    'https://paypa1.com/signin',
    'http://192.168.1.1/secure/login.php',
    'https://goog1e.com/signin',
    'http://198.51.100.1/admin',
    'https://micr0soft.com/office365',
    'http://14.18.98.5/bank/login',
    'https://app1e.com/icloud',
    'https://secure-bank-login.com/verify',
    'http://194.168.5.5/update',
    'https://admin-panel.com/login',
    'http://random-characters-xyz.com/phishing',
    'https://0-paypal-0.com/verify',
    'http://199.199.199.199/hack',
    'https://bank%20secure.com/login',
    'https://legitimate@evil.com/phish',
    'http://194.45.50.1:8080/admin',
    'https://www-bank-secure-login.com/verify',
    'http://195.166.5.5/banking',
    'https://account.confirm-identity.com',
    'http://10.10.10.10/confidential',
    'https://mail.verify-account-urgently.com',
    'http://redirect.to.evil-site.com',
    'https://update.system.alert.now.com/download',
]

# Sample legitimate URLs (for demonstration)
SAMPLE_LEGITIMATE_URLS = [
    'https://google.com',
    'https://www.google.com',
    'https://github.com',
    'https://www.github.com',
    'https://stackoverflow.com',
    'https://www.wikipedia.org',
    'https://amazon.com',
    'https://www.amazon.com',
    'https://facebook.com',
    'https://www.facebook.com',
    'https://youtube.com',
    'https://www.youtube.com',
    'https://twitter.com',
    'https://www.linkedin.com',
    'https://reddit.com',
    'https://www.reddit.com',
    'https://instagram.com',
    'https://www.instagram.com',
    'https://github.com/profile',
    'https://docs.python.org',
    'https://www.python.org',
    'https://www.medium.com',
    'https://dev.to',
    'https://www.npmjs.com',
    'https://pypi.org',
    'https://www.tensorflow.org',
]

def main():
    print("="*60)
    print("PHISHING URL SCANNER - MODEL TRAINING")
    print("="*60)
    
    # Initialize trainer
    trainer = ModelTrainer(Config)
    
    # Prepare dataset
    print("\nStep 1: Preparing training dataset...")
    X, y = trainer.prepare_dataset(
        urls_legitimate=SAMPLE_LEGITIMATE_URLS,
        urls_phishing=SAMPLE_PHISHING_URLS
    )
    
    # Train models
    print("\nStep 2: Training models...")
    models = trainer.train_models(X, y)
    
    # Save models
    print("\nStep 3: Saving models...")
    trainer.save_models(models)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run the Flask API: python src/app.py")
    print("2. Test the API: python scripts/test_api.py")
    print("3. Or use the example notebook: notebooks/example_usage.ipynb")

if __name__ == '__main__':
    main()
