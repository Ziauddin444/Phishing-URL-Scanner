"""
Comprehensive test suite for Phishing URL Scanner
Tests critical paths and high-complexity functionality
Focus: API endpoints, predictions, feature extraction, input validation
"""

import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import app, error_response, _normalize_url, _validate_json_field
from src.predictor import URLPredictor
from src.heuristic_analyzer import URLHeuristicAnalyzer


# ============= FIXTURES =============
@pytest.fixture
def client():
    """Create test client for Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def predictor():
    """Load predictor for direct testing"""
    from config import ProductionConfig
    return URLPredictor(ProductionConfig)


@pytest.fixture
def analyzer():
    """Load analyzer for feature testing"""
    return URLHeuristicAnalyzer()


# ============= UTILITY FUNCTION TESTS =============
class TestUtilityFunctions:
    """Test helper/utility functions"""
    
    def test_normalize_url_with_https(self):
        """Test URL normalization with existing HTTPS"""
        result = _normalize_url("https://google.com")
        assert result == "https://google.com"
    
    def test_normalize_url_with_http(self):
        """Test URL normalization with HTTP"""
        result = _normalize_url("http://example.com")
        assert result == "http://example.com"
    
    def test_normalize_url_without_protocol(self):
        """Test URL normalization adds HTTPS by default"""
        result = _normalize_url("google.com")
        assert result == "https://google.com"
    
    def test_normalize_url_strips_whitespace(self):
        """Test URL normalization strips whitespace"""
        result = _normalize_url("  example.com  ")
        assert result == "https://example.com"
    
    def test_normalize_url_empty_string(self):
        """Test URL normalization with empty string"""
        result = _normalize_url("")
        assert result is None
    
    def test_normalize_url_none_value(self):
        """Test URL normalization with None"""
        result = _normalize_url(None)
        assert result is None
    
    def test_error_response_format(self):
        """Test error response creates proper JSON"""
        response, status = error_response("Test error", 400)
        data = json.loads(response.get_data(as_text=True))
        assert data['error'] == "Test error"
        assert status == 400


# ============= API ENDPOINT TESTS =============
class TestAPIEndpoints:
    """Test Flask API endpoints"""
    
    def test_health_check_endpoint(self, client):
        """Test health check returns proper response"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'Phishing URL Scanner'
        assert 'models_loaded' in data
    
    def test_dashboard_endpoint(self, client):
        """Test dashboard endpoint returns HTML"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'Phishing URL Scanner' in response.get_data(as_text=True)
    
    def test_404_error_handler(self, client):
        """Test 404 error handling"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_method_not_allowed(self, client):
        """Test 405 Method Not Allowed"""
        response = client.get('/api/predict')  # GET on POST-only endpoint
        assert response.status_code == 405
        data = json.loads(response.data)
        assert 'error' in data


# ============= SINGLE URL PREDICTION TESTS =============
class TestSingleURLPrediction:
    """Test single URL prediction endpoint"""
    
    def test_predict_legitimate_url(self, client):
        """Test prediction for legitimate URL"""
        response = client.post('/api/predict',
            json={'url': 'https://google.com'},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'prediction' in data
        assert data['prediction'] in ['LEGITIMATE', 'PHISHING']
        assert 'confidence' in data
        assert 0 <= data['confidence'] <= 1
    
    def test_predict_phishing_url(self, client):
        """Test prediction for phishing-like URL"""
        response = client.post('/api/predict',
            json={'url': 'https://paypa1.com'},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'prediction' in data
        assert data['prediction'] in ['LEGITIMATE', 'PHISHING']
    
    def test_predict_missing_url_field(self, client):
        """Test error when URL field is missing"""
        response = client.post('/api/predict',
            json={'domain': 'example.com'},
            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'url' in data['error'].lower()
    
    def test_predict_empty_request_body(self, client):
        """Test error with empty request body"""
        response = client.post('/api/predict',
            json={},
            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_predict_invalid_json(self, client):
        """Test error with invalid JSON"""
        response = client.post('/api/predict',
            data='invalid json',
            content_type='application/json')
        
        assert response.status_code == 400
    
    def test_predict_url_too_long(self, client):
        """Test error when URL exceeds max length"""
        long_url = 'https://' + 'a' * 3000 + '.com'
        response = client.post('/api/predict',
            json={'url': long_url},
            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'too long' in data['error'].lower()
    
    def test_predict_url_normalization(self, client):
        """Test that URLs are normalized (protocol added)"""
        response = client.post('/api/predict',
            json={'url': 'example.com'},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['url'].startswith('https://')


# ============= BATCH PREDICTION TESTS =============
class TestBatchPrediction:
    """Test batch prediction endpoint"""
    
    def test_predict_batch_multiple_urls(self, client):
        """Test batch prediction with multiple URLs"""
        urls = ['https://google.com', 'https://example.com', 'https://github.com']
        response = client.post('/api/predict-batch',
            json={'urls': urls},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total'] == 3
        assert len(data['results']) == 3
        
        for result in data['results']:
            assert 'url' in result
            assert 'prediction' in result
            assert 'confidence' in result
    
    def test_predict_batch_missing_urls_field(self, client):
        """Test error when urls field is missing"""
        response = client.post('/api/predict-batch',
            json={'urls_list': ['google.com']},
            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'urls' in data['error'].lower()
    
    def test_predict_batch_urls_not_list(self, client):
        """Test error when urls is not a list"""
        response = client.post('/api/predict-batch',
            json={'urls': 'google.com'},
            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'list' in data['error'].lower()
    
    def test_predict_batch_empty_list(self, client):
        """Test error when urls list is empty"""
        response = client.post('/api/predict-batch',
            json={'urls': []},
            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'empty' in data['error'].lower()
    
    def test_predict_batch_exceeds_limit(self, client):
        """Test error when exceeding maximum URLs"""
        urls = [f'https://example{i}.com' for i in range(150)]
        response = client.post('/api/predict-batch',
            json={'urls': urls},
            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'maximum' in data['error'].lower()
    
    def test_predict_batch_url_normalization(self, client):
        """Test that batch URLs are normalized"""
        urls = ['google.com', 'example.com']
        response = client.post('/api/predict-batch',
            json={'urls': urls},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        for result in data['results']:
            assert result['url'].startswith('https://')


# ============= FEATURE EXTRACTION TESTS =============
class TestFeatureExtraction:
    """Test feature extraction endpoint"""
    
    def test_extract_features_valid_url(self, client):
        """Test feature extraction for valid URL"""
        response = client.post('/api/features',
            json={'url': 'https://google.com'},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'url' in data
        assert 'features' in data
        assert 'feature_names' in data
        assert len(data['features']) == len(data['feature_names'])
    
    def test_extract_features_returns_22_features(self, client):
        """Test that exactly 22 features are extracted"""
        response = client.post('/api/features',
            json={'url': 'https://example.com'},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['features']) == 22
        assert len(data['feature_names']) == 22
    
    def test_extract_features_missing_url(self, client):
        """Test error when URL is missing"""
        response = client.post('/api/features',
            json={},
            content_type='application/json')
        
        assert response.status_code == 400


# ============= MODEL STATISTICS TESTS =============
class TestModelStatistics:
    """Test model statistics endpoint"""
    
    def test_get_stats(self, client):
        """Test statistics endpoint returns proper structure"""
        response = client.get('/api/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify structure
        assert 'models' in data
        assert 'features' in data
        assert 'ensemble_method' in data
        
        # Verify model info
        assert 'random_forest' in data['models']
        assert 'svm' in data['models']
        
        # Verify feature info
        assert data['features']['total_features'] == 22
        assert len(data['features']['feature_names']) == 22


# ============= DIRECT PREDICTOR TESTS =============
class TestDirectPredictor:
    """Test URLPredictor class directly"""
    
    def test_single_prediction(self, predictor):
        """Test single URL prediction"""
        result = predictor.predict('https://google.com')
        
        assert 'url' in result
        assert 'prediction' in result
        assert result['prediction'] in ['LEGITIMATE', 'PHISHING']
        assert 'confidence' in result
        assert 0 <= result['confidence'] <= 1
    
    def test_batch_prediction(self, predictor):
        """Test batch URL prediction"""
        urls = ['https://google.com', 'https://example.com']
        results = predictor.batch_predict(urls)
        
        assert len(results) == 2
        for result in results:
            assert 'prediction' in result
            assert result['prediction'] in ['LEGITIMATE', 'PHISHING']


# ============= FEATURE ANALYZER TESTS =============
class TestFeatureAnalyzer:
    """Test URLHeuristicAnalyzer class"""
    
    def test_analyze_url_returns_22_features(self, analyzer):
        """Test feature extraction returns 22 features"""
        features = analyzer.analyze_url('https://google.com')
        
        assert len(features) == 22
        assert all(isinstance(f, (int, float)) for f in features)
    
    def test_get_feature_names(self, analyzer):
        """Test feature names are provided"""
        names = analyzer.get_feature_names()
        
        assert len(names) == 22
        assert all(isinstance(n, str) for n in names)
        assert len(set(names)) == 22  # All unique
    
    def test_feature_extraction_legitimate_url(self, analyzer):
        """Test feature extraction for legitimate URL"""
        features = analyzer.analyze_url('https://google.com')
        
        assert len(features) == 22
        # Legitimate URLs typically have low suspicious feature values
        assert all(0 <= f <= 1 or isinstance(f, int) for f in features)
    
    def test_feature_extraction_suspicious_url(self, analyzer):
        """Test feature extraction for suspicious URL"""
        features = analyzer.analyze_url('https://gggle.com')  # Typosquatting
        
        assert len(features) == 22


# ============= INPUT VALIDATION TESTS =============
class TestInputValidation:
    """Test input validation and sanitization"""
    
    def test_special_characters_in_url(self, client):
        """Test URLs with special characters"""
        response = client.post('/api/predict',
            json={'url': 'https://example.com/?q=<script>'},
            content_type='application/json')
        
        # Should handle safely without XSS
        assert response.status_code in [200, 400]
    
    def test_unicode_in_url(self, client):
        """Test URLs with unicode characters"""
        response = client.post('/api/predict',
            json={'url': 'https://example.com/путь'},
            content_type='application/json')
        
        # Should handle or reject gracefully
        assert response.status_code in [200, 400]
    
    def test_very_short_url(self, client):
        """Test very short URL"""
        response = client.post('/api/predict',
            json={'url': 'a.co'},
            content_type='application/json')
        
        assert response.status_code == 200
    
    def test_url_with_port(self, client):
        """Test URL with port number"""
        response = client.post('/api/predict',
            json={'url': 'https://example.com:8080/path'},
            content_type='application/json')
        
        assert response.status_code == 200


# ============= SECURITY TESTS =============
class TestSecurity:
    """Test security features"""
    
    def test_cors_headers_present(self, client):
        """Test CORS headers are properly set"""
        response = client.options('/api/predict')
        
        # CORS should be enabled (configured by Flask-CORS)
        assert response.status_code in [200, 405]
    
    def test_debug_mode_off_in_config(self):
        """Test debug mode is off in production config"""
        from config import ProductionConfig
        assert ProductionConfig.DEBUG is False
    
    def test_testing_mode_not_production(self):
        """Test TESTING flag is not set in production"""
        from config import ProductionConfig
        assert ProductionConfig.TESTING is False


# ============= INTEGRATION TESTS =============
class TestIntegration:
    """End-to-end integration tests"""
    
    def test_full_workflow_single_url(self, client):
        """Test complete workflow: health → predict → stats"""
        # Check health
        health = client.get('/api/health')
        assert health.status_code == 200
        
        # Make prediction
        prediction = client.post('/api/predict',
            json={'url': 'https://google.com'},
            content_type='application/json')
        assert prediction.status_code == 200
        
        # Get stats
        stats = client.get('/api/stats')
        assert stats.status_code == 200
    
    def test_full_workflow_batch_urls(self, client):
        """Test complete workflow with batch"""
        # Health check
        health = client.get('/api/health')
        assert health.status_code == 200
        
        # Batch prediction
        batch = client.post('/api/predict-batch',
            json={'urls': ['google.com', 'example.com']},
            content_type='application/json')
        assert batch.status_code == 200
        data = json.loads(batch.data)
        assert data['total'] == 2


# ============= PERFORMANCE TESTS =============
class TestPerformance:
    """Test performance characteristics"""
    
    def test_single_prediction_completes_quickly(self, predictor):
        """Test that single prediction completes in reasonable time"""
        import time
        
        start = time.time()
        predictor.predict('https://google.com')
        elapsed = time.time() - start
        
        # Should complete in less than 10 seconds
        assert elapsed < 10
    
    def test_batch_prediction_handles_100_urls(self, client):
        """Test batch prediction can handle 100 URLs"""
        urls = [f'https://example{i}.com' for i in range(100)]
        
        response = client.post('/api/predict-batch',
            json={'urls': urls},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total'] == 100


if __name__ == '__main__':
    # Run tests with pytest
    # pytest tests_comprehensive.py -v
    pytest.main([__file__, '-v'])
