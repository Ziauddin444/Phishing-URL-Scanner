#!/usr/bin/env python3
"""
Core Validation Script - Verify critical functionality without pytest
This script tests the most critical paths without external dependencies
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def validate_imports():
    """Validate all critical imports work"""
    print("=" * 60)
    print("VALIDATION: Core Module Imports")
    print("=" * 60)
    
    try:
        from config import DevelopmentConfig, ProductionConfig
        print("✅ Config imports successful")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from predictor import URLPredictor
        print("✅ URLPredictor import successful")
    except ImportError as e:
        print(f"❌ URLPredictor import failed: {e}")
        return False
    
    try:
        from heuristic_analyzer import URLHeuristicAnalyzer
        print("✅ URLHeuristicAnalyzer import successful")
    except ImportError as e:
        print(f"❌ URLHeuristicAnalyzer import failed: {e}")
        return False
    
    try:
        from app import app
        print("✅ Flask app import successful")
    except ImportError as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    
    return True


def validate_config_security():
    """Validate security configuration"""
    print("\n" + "=" * 60)
    print("VALIDATION: Configuration Security")
    print("=" * 60)
    
    from config import DevelopmentConfig, ProductionConfig, _get_secure_secret_key
    
    # Check production config defaults
    prod_cfg = ProductionConfig()
    if prod_cfg.DEBUG:
        print("❌ Production DEBUG mode enabled (should be False)")
        return False
    print("✅ Production DEBUG mode disabled")
    
    if prod_cfg.TESTING:
        print("❌ Production TESTING mode enabled (should be False)")
        return False
    print("✅ Production TESTING mode disabled")
    
    # Check development config
    dev_cfg = DevelopmentConfig()
    if not dev_cfg.DEBUG:
        print("❌ Development DEBUG mode disabled (should be True)")
        return False
    print("✅ Development DEBUG mode enabled")
    
    # Check SECRET_KEY validation
    try:
        key = _get_secure_secret_key('development')
        print("✅ SECRET_KEY validation function works")
    except Exception as e:
        print(f"❌ SECRET_KEY validation failed: {e}")
        return False
    
    return True


def validate_predictor():
    """Validate URL predictor functionality"""
    print("\n" + "=" * 60)
    print("VALIDATION: URL Predictor")
    print("=" * 60)
    
    from predictor import URLPredictor
    from config import DevelopmentConfig
    
    try:
        cfg = DevelopmentConfig()
        predictor = URLPredictor(cfg)
        print("✅ URLPredictor initialized successfully")
    except Exception as e:
        print(f"❌ URLPredictor initialization failed: {e}")
        return False
    
    # Test single prediction
    try:
        result = predictor.predict('https://google.com')
        
        if not isinstance(result, dict):
            print("❌ Prediction result is not a dictionary")
            return False
        
        required_keys = ['prediction', 'probability', 'models']
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing key in prediction result: {key}")
                return False
        
        print(f"✅ Single prediction works: {result['prediction']} ({result['probability']:.2%})")
    except Exception as e:
        print(f"❌ Single prediction failed: {e}")
        return False
    
    # Test batch prediction
    try:
        urls = ['https://google.com', 'https://microsoft.com', 'http://example.com']
        results = predictor.batch_predict(urls)
        
        if not isinstance(results, list):
            print("❌ Batch prediction result is not a list")
            return False
        
        if len(results) != len(urls):
            print(f"❌ Batch prediction count mismatch: expected {len(urls)}, got {len(results)}")
            return False
        
        print(f"✅ Batch prediction works: processed {len(results)} URLs")
    except Exception as e:
        print(f"❌ Batch prediction failed: {e}")
        return False
    
    return True


def validate_feature_analyzer():
    """Validate feature extraction"""
    print("\n" + "=" * 60)
    print("VALIDATION: Feature Analyzer")
    print("=" * 60)
    
    from heuristic_analyzer import URLHeuristicAnalyzer
    
    try:
        analyzer = URLHeuristicAnalyzer()
        print("✅ URLHeuristicAnalyzer initialized successfully")
    except Exception as e:
        print(f"❌ URLHeuristicAnalyzer initialization failed: {e}")
        return False
    
    # Get feature names
    try:
        feature_names = analyzer.get_feature_names()
        feature_count = len(feature_names)
        
        if feature_count != 22:
            print(f"❌ Expected 22 features, got {feature_count}")
            return False
        
        print(f"✅ Feature analyzer has {feature_count} features")
    except Exception as e:
        print(f"❌ Failed to get feature names: {e}")
        return False
    
    # Test feature extraction
    try:
        features = analyzer.analyze_url('https://google.com')
        
        if len(features) != 22:
            print(f"❌ Expected 22 features in analysis, got {len(features)}")
            return False
        
        print(f"✅ Feature extraction works: extracted {len(features)} features")
    except Exception as e:
        print(f"❌ Feature extraction failed: {e}")
        return False
    
    return True


def validate_dashboard():
    """Validate dashboard file exists and has security functions"""
    print("\n" + "=" * 60)
    print("VALIDATION: Dashboard Security")
    print("=" * 60)
    
    # Check both possible locations
    dashboard_path = Path(__file__).parent / 'dashboard.html'
    if not dashboard_path.exists():
        dashboard_path = Path(__file__).parent / 'templates' / 'dashboard.html'
    
    if not dashboard_path.exists():
        print(f"❌ Dashboard file not found at expected locations")
        return False
    
    dashboard_content = dashboard_path.read_text()
    
    security_functions = ['escapeHtml', 'sanitizeUrl', 'validateNumberInput', 'createElement']
    
    all_present = True
    for func in security_functions:
        if f"function {func}" in dashboard_content:
            print(f"✅ Security function '{func}' found")
        else:
            print(f"❌ Security function '{func}' not found")
            all_present = False
    
    return all_present


def validate_flask_app():
    """Validate Flask app endpoints"""
    print("\n" + "=" * 60)
    print("VALIDATION: Flask App Endpoints")
    print("=" * 60)
    
    from app import app
    
    client = app.test_client()
    
    # Test health endpoint
    try:
        response = client.get('/api/health')
        if response.status_code != 200:
            print(f"❌ Health endpoint returned {response.status_code}")
            return False
        
        data = json.loads(response.data)
        print(f"✅ Health endpoint works: {data.get('status', 'ok')}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False
    
    # Test dashboard endpoint
    try:
        response = client.get('/')
        if response.status_code != 200:
            print(f"❌ Dashboard endpoint returned {response.status_code}")
            return False
        
        print(f"✅ Dashboard endpoint works: returns HTML")
    except Exception as e:
        print(f"❌ Dashboard endpoint failed: {e}")
        return False
    
    # Test 404 handling
    try:
        response = client.get('/nonexistent')
        if response.status_code != 404:
            print(f"❌ 404 endpoint returned {response.status_code}")
            return False
        
        print(f"✅ 404 error handling works")
    except Exception as e:
        print(f"❌ 404 error handling failed: {e}")
        return False
    
    return True


def main():
    """Run all validations"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " PHISHING URL SCANNER - CORE VALIDATION ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    validations = [
        ("Module Imports", validate_imports),
        ("Config Security", validate_config_security),
        ("URL Predictor", validate_predictor),
        ("Feature Analyzer", validate_feature_analyzer),
        ("Dashboard Security", validate_dashboard),
        ("Flask Endpoints", validate_flask_app),
    ]
    
    results = {}
    for name, validate_func in validations:
        try:
            result = validate_func()
            results[name] = result
        except Exception as e:
            print(f"\n❌ EXCEPTION in {name}: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("-" * 60)
    print(f"Result: {passed}/{total} validations passed")
    
    if passed == total:
        print("\n🎉 ALL VALIDATIONS PASSED - Core functionality is working!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed - review errors above")
        return 1


if __name__ == '__main__':
    sys.exit(main())
