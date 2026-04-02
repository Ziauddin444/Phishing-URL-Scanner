"""
API Testing Script
Test the Flask API endpoints
"""
import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    response = requests.get(f'{BASE_URL}/health')
    print(json.dumps(response.json(), indent=2))

def test_single_prediction():
    """Test single URL prediction"""
    print("\n" + "="*60)
    print("TEST 2: Single URL Prediction")
    print("="*60)
    
    test_urls = [
        'https://google.com',  # Legitimate
        'https://paypa1.com',  # Phishing
        'http://194.168.5.5/bank',  # Phishing (IP address)
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        response = requests.post(f'{BASE_URL}/predict', json={'url': url})
        result = response.json()
        print(f"Prediction: {result.get('prediction')}")
        print(f"Confidence: {result.get('confidence_percentage')}%")
        print(f"RF Model: {result.get('models', {}).get('random_forest', {}).get('prediction')}")
        print(f"SVM Model: {result.get('models', {}).get('svm', {}).get('prediction')}")

def test_batch_prediction():
    """Test batch URL prediction"""
    print("\n" + "="*60)
    print("TEST 3: Batch URL Prediction")
    print("="*60)
    
    urls = [
        'https://github.com',
        'https://facebook.com',
        'https://am4zon.com',
        'http://10.0.0.1/admin',
    ]
    
    response = requests.post(f'{BASE_URL}/predict-batch', json={'urls': urls})
    result = response.json()
    
    print(f"\nTotal URLs scanned: {result.get('total')}")
    for pred in result.get('results', []):
        print(f"\n  URL: {pred.get('url')}")
        print(f"  Prediction: {pred.get('prediction')}")
        print(f"  Confidence: {pred.get('confidence_percentage')}%")

def test_features():
    """Test feature extraction"""
    print("\n" + "="*60)
    print("TEST 4: Feature Extraction")
    print("="*60)
    
    url = 'https://suspicious-banking-site.com'
    response = requests.post(f'{BASE_URL}/features', json={'url': url})
    result = response.json()
    
    print(f"\nURL: {result.get('url')}")
    print(f"Total Features: {len(result.get('features', {}))}")
    print("\nSample Features:")
    features = result.get('features', {})
    for i, (key, value) in enumerate(list(features.items())[:10]):
        print(f"  {key}: {value}")

def test_stats():
    """Test model statistics"""
    print("\n" + "="*60)
    print("TEST 5: Model Statistics")
    print("="*60)
    response = requests.get(f'{BASE_URL}/stats')
    print(json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    print("\n\nPHISHING URL SCANNER - API TEST SUITE")
    print("Make sure Flask API is running on localhost:5000")
    
    try:
        test_health()
        test_single_prediction()
        test_batch_prediction()
        test_features()
        test_stats()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API at http://localhost:5000")
        print("Make sure Flask app is running: python src/app.py")
