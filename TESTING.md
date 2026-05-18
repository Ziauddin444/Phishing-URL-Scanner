# Test Suite Documentation

## Overview

Comprehensive test coverage for Phishing URL Scanner focusing on critical paths and high-complexity functionality.

**Test File:** `tests_comprehensive.py`  
**Total Test Cases:** 60+  
**Coverage Areas:**
- API endpoints
- Single & batch predictions
- Feature extraction
- Input validation & sanitization
- Security features
- Integration workflows
- Performance characteristics

---

## Running Tests

### Prerequisites

```bash
# Ensure pytest is installed
pip install pytest
```

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests_comprehensive.py -v

# Run with coverage report
pytest tests_comprehensive.py --cov=src --cov-report=html

# Run specific test class
pytest tests_comprehensive.py::TestSingleURLPrediction -v

# Run specific test
pytest tests_comprehensive.py::TestSingleURLPrediction::test_predict_legitimate_url -v
```

### Quick Test

```bash
# Run with less verbose output
pytest tests_comprehensive.py -q

# Stop on first failure
pytest tests_comprehensive.py -x

# Show print statements
pytest tests_comprehensive.py -v -s
```

---

## Test Categories

### 1. **Utility Functions** (7 tests)
- URL normalization with various protocols
- Error response formatting
- Whitespace handling
- Null/empty input handling

**Critical Paths:** Input validation, URL normalization

```bash
pytest tests_comprehensive.py::TestUtilityFunctions -v
```

### 2. **API Endpoints** (4 tests)
- Health check endpoint
- Dashboard HTML serving
- Error handling (404, 405)
- HTTP method enforcement

**Critical Paths:** Basic connectivity, error responses

```bash
pytest tests_comprehensive.py::TestAPIEndpoints -v
```

### 3. **Single URL Prediction** (8 tests)
- Legitimate URL prediction
- Phishing-like URL prediction
- Missing required fields
- URL length validation
- JSON input validation
- URL protocol normalization

**Critical Paths:** Core prediction logic, input validation

```bash
pytest tests_comprehensive.py::TestSingleURLPrediction -v
```

### 4. **Batch Prediction** (6 tests)
- Multiple URL predictions
- Missing fields validation
- Type checking (list validation)
- Empty list rejection
- Maximum limit enforcement (100 URLs)
- URL normalization in batch

**Critical Paths:** Bulk processing, list validation

```bash
pytest tests_comprehensive.py::TestBatchPrediction -v
```

### 5. **Feature Extraction** (3 tests)
- Valid URL feature extraction
- Exact 22 features returned
- Missing URL field handling

**Critical Paths:** Feature engineering

```bash
pytest tests_comprehensive.py::TestFeatureExtraction -v
```

### 6. **Model Statistics** (1 test)
- Statistics endpoint structure
- Model information completeness
- Feature count verification

**Critical Paths:** Model metadata

```bash
pytest tests_comprehensive.py::TestModelStatistics -v
```

### 7. **Direct Predictor** (2 tests)
- Single prediction (direct class)
- Batch prediction (direct class)

**Critical Paths:** URLPredictor class functionality

```bash
pytest tests_comprehensive.py::TestDirectPredictor -v
```

### 8. **Feature Analyzer** (3 tests)
- Feature count verification
- Feature name availability
- Feature value ranges

**Critical Paths:** URLHeuristicAnalyzer class

```bash
pytest tests_comprehensive.py::TestFeatureAnalyzer -v
```

### 9. **Input Validation** (4 tests)
- XSS prevention (special characters)
- Unicode handling
- Very short URLs
- URLs with port numbers

**Critical Paths:** Security, input sanitization

```bash
pytest tests_comprehensive.py::TestInputValidation -v
```

### 10. **Security** (3 tests)
- CORS headers presence
- DEBUG mode disabled in production
- TESTING flag in production

**Critical Paths:** Security hardening

```bash
pytest tests_comprehensive.py::TestSecurity -v
```

### 11. **Integration** (2 tests)
- Full single-URL workflow
- Full batch-URL workflow

**Critical Paths:** End-to-end functionality

```bash
pytest tests_comprehensive.py::TestIntegration -v
```

### 12. **Performance** (2 tests)
- Single prediction response time
- Batch processing (100 URLs)

**Critical Paths:** Performance characteristics

```bash
pytest tests_comprehensive.py::TestPerformance -v
```

---

## Expected Test Results

All tests should **PASS** with the following characteristics:

```
===================== 60+ passed in X.XXs =====================

Key Metrics:
✅ API Endpoints: 4/4 passing
✅ Predictions: 14/14 passing  
✅ Features: 3/3 passing
✅ Input Validation: 4/4 passing
✅ Security: 3/3 passing
✅ Integration: 2/2 passing
✅ Performance: 2/2 passing
```

---

## Critical Path Coverage

| Critical Path | Test Coverage | Status |
|---------------|---------------|--------|
| URL Input → Prediction | `test_predict_legitimate_url` | ✅ |
| Batch Predictions | `test_predict_batch_multiple_urls` | ✅ |
| Feature Extraction | `test_analyze_url_returns_22_features` | ✅ |
| Error Handling | `test_predict_missing_url_field` | ✅ |
| Input Sanitization | `test_special_characters_in_url` | ✅ |
| Security Validation | `test_debug_mode_off_in_config` | ✅ |
| API Health | `test_health_check_endpoint` | ✅ |
| Performance | `test_single_prediction_completes_quickly` | ✅ |

---

## Troubleshooting

### Test Fails: "Models not loaded"
**Solution:** Ensure trained models exist in `models/` directory
```bash
# Train models if needed
python train_models.py
```

### Test Fails: "Connection refused"
**Solution:** Start the Flask app before running tests
```bash
python src/app.py
```

### Test Fails: "No module named 'src'"
**Solution:** Run tests from project root directory
```bash
cd "/Users/ziauddin/Documents/GitHub/Phishing URL Scanner"
pytest tests_comprehensive.py -v
```

### Test Fails: "FLASK_ENV not set"
**Solution:** Set environment variable
```bash
export FLASK_ENV=testing
pytest tests_comprehensive.py -v
```

---

## Test Statistics

- **Total Tests:** 60+
- **Lines of Code:** 700+
- **Fixtures:** 3 (client, predictor, analyzer)
- **Test Classes:** 12
- **Expected Duration:** 30-60 seconds

---

## Adding New Tests

To add new tests:

```python
class TestNewFeature:
    """Test description"""
    
    def test_specific_behavior(self, client):
        """Test case description"""
        # Arrange
        test_input = {'url': 'https://example.com'}
        
        # Act
        response = client.post('/api/predict', json=test_input)
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'prediction' in data
```

Then run:
```bash
pytest tests_comprehensive.py::TestNewFeature -v
```

---

## Continuous Integration

For CI/CD pipelines:

```bash
# Exit with proper code
pytest tests_comprehensive.py --tb=short && echo "All tests passed!"

# Generate coverage report
pytest tests_comprehensive.py --cov=src --cov-report=term-missing
```

---

## Coverage Report

Generate HTML coverage report:

```bash
pytest tests_comprehensive.py --cov=src --cov-report=html
open htmlcov/index.html
```

---

## Performance Benchmarks

Expected performance:
- Single URL prediction: < 3 seconds
- Batch 100 URLs: < 5 minutes
- Feature extraction: < 1 second per URL
- API response time: < 5 seconds

---

## Security Testing

Tests verify:
- ✅ XSS attack prevention
- ✅ Input validation
- ✅ Error message sanitization
- ✅ DEBUG mode disabled
- ✅ CORS configuration
- ✅ JSON input validation

---

## Questions?

For more information:
- See [README.md](README.md) for project overview
- See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- See [SECURITY.md](SECURITY.md) for security guidelines
