#!/usr/bin/env python3
"""
Test script for Phishing URL Scanner API
"""
import requests
import json
import time
import sys

# Wait for server to start
time.sleep(2)

BASE_URL = 'http://localhost:3000/api'

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(json.dumps(response.json(), indent=2))
        print('✅ Health check passed\n')
        return True
    except Exception as e:
        print(f'❌ Health check failed: {e}\n')
        return False

def test_single_prediction():
    """Test single URL prediction"""
    print("="*60)
    print("TEST 2: Single URL Prediction")
    print("="*60)
    
    test_urls = [
        'https://google.com',  # Legitimate
        'https://paypa1.com',  # Phishing
        'http://194.168.5.5/bank',  # Phishing (IP address)
    ]
    
    all_passed = True
    for url in test_urls:
        try:
            print(f'\nTesting URL: {url}')
            response = requests.post(f'{BASE_URL}/predict', json={'url': url})
            if response.status_code == 200:
                result = response.json()
                print(f'  Prediction: {result.get("prediction")}')
                print(f'  Confidence: {result.get("confidence_percentage")}%')
                print('  ✅ Passed')
            else:
                print(f'  ❌ Failed with status {response.status_code}: {response.text}')
                all_passed = False
        except Exception as e:
            print(f'  ❌ Error: {e}')
            all_passed = False
    
    print()
    return all_passed

def test_batch_prediction():
    """Test batch URL prediction"""
    print("="*60)
    print("TEST 3: Batch URL Prediction")
    print("="*60)
    
    urls = [
        'https://github.com',
        'https://facebook.com',
        'https://am4zon.com',
        'http://10.0.0.1/admin',
    ]
    
    try:
        response = requests.post(f'{BASE_URL}/predict-batch', json={'urls': urls})
        if response.status_code == 200:
            results = response.json()
            print(json.dumps(results, indent=2))
            print('✅ Batch prediction passed\n')
            return True
        else:
            print(f'❌ Failed with status {response.status_code}: {response.text}\n')
            return False
    except Exception as e:
        print(f'❌ Batch prediction failed: {e}\n')
        return False

def test_features():
    """Test feature analysis endpoint"""
    print("="*60)
    print("TEST 4: Feature Analysis")
    print("="*60)
    
    test_url = 'https://google.com'
    
    try:
        response = requests.post(f'{BASE_URL}/features', json={'url': test_url})
        if response.status_code == 200:
            result = response.json()
            print(f'URL: {test_url}')
            print(json.dumps(result, indent=2)[:500] + '...')
            print('✅ Feature analysis passed\n')
            return True
        else:
            print(f'❌ Failed with status {response.status_code}: {response.text}\n')
            return False
    except Exception as e:
        print(f'❌ Feature analysis failed: {e}\n')
        return False

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║           🧪 PHISHING URL SCANNER - API TEST SUITE 🧪                          ║
╚════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    results = {
        'Health Check': test_health(),
        'Single Prediction': test_single_prediction(),
        'Batch Prediction': test_batch_prediction(),
        'Feature Analysis': test_features(),
    }
    
    print("="*60)
    print("SUMMARY")
    print("="*60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f'\nPassed: {passed}/{total}')
    for test_name, passed_status in results.items():
        status = '✅' if passed_status else '❌'
        print(f'{status} {test_name}')
    
    if passed == total:
        print('\n🎉 ALL TESTS PASSED! Project is fully functional.')
        sys.exit(0)
    else:
        print(f'\n⚠️  {total - passed} test(s) failed.')
        sys.exit(1)
