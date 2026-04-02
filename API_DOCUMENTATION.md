# API DOCUMENTATION

## Phishing URL Scanner REST API

Complete API reference for the Phishing URL Scanner Flask application.

---

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently no authentication required. In production, implement API key authentication.

---

## Endpoints

### 1. Health Check

**Endpoint**: `GET /api/health`

**Description**: Check if API is running and models are loaded.

**Response**: 
```json
{
  "status": "healthy",
  "service": "Phishing URL Scanner",
  "version": "1.0.0",
  "models_loaded": true
}
```

**Status Code**: 200

**Example**:
```bash
curl http://localhost:5000/api/health
```

---

### 2. Single URL Prediction

**Endpoint**: `POST /api/predict`

**Description**: Predict whether a single URL is phishing or legitimate.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "url": "https://example.com"
}
```

**Parameters**:
- `url` (string, required): The URL to analyze. Can include or exclude protocol.

**Response**:
```json
{
  "url": "https://example.com",
  "prediction": "LEGITIMATE",
  "confidence": 0.95,
  "confidence_percentage": 95.0,
  "models": {
    "random_forest": {
      "prediction": "LEGITIMATE",
      "confidence": 0.97
    },
    "svm": {
      "prediction": "LEGITIMATE",
      "confidence": 0.93
    }
  },
  "features": {
    "url_length": 20,
    "has_ip": 0,
    "domain_length": 11,
    "subdomain_count": 1,
    "has_suspicious_chars": 0,
    "special_chars_in_domain": 0,
    "url_entropy": 3.45,
    "double_slash_in_path": 0,
    "has_https": 1,
    "query_length": 0,
    "has_query_string": 0,
    "equals_in_url": 0,
    "at_symbol": 0,
    "dots_in_domain": 1,
    "hyphens_in_domain": 0,
    "percent_sign": 0,
    "valid_tld": 1,
    "short_domain_high_entropy": 0,
    "has_port": 0,
    "has_redirect": 0,
    "digits_in_domain": 0,
    "domain_mixed_suspicious": 0
  },
  "top_features": [
    ["has_https", 0.18],
    ["url_length", 0.12],
    ["subdomain_count", 0.10]
  ]
}
```

**Status Codes**:
- `200`: Successfully predicted
- `400`: Invalid URL or missing required field
- `500`: Models not loaded

**Examples**:

```bash
# With protocol
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'

# Without protocol (automatically added)
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "google.com"}'
```

**Response Explanation**:
- `prediction`: Final ensemble prediction (PHISHING or LEGITIMATE)
- `confidence`: Confidence score (0-1), where 1 is most confident
- `confidence_percentage`: Confidence as percentage (0-100)
- `models`: Individual model predictions and their confidence
- `features`: All 22 extracted features (for transparency)
- `top_features`: 5 most important features for this prediction

---

### 3. Batch URL Prediction

**Endpoint**: `POST /api/predict-batch`

**Description**: Predict multiple URLs in one request.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "urls": [
    "https://google.com",
    "https://suspicious-site.com",
    "amazon.com"
  ]
}
```

**Parameters**:
- `urls` (array, required): List of URLs to analyze. Maximum 100 URLs per request.

**Response**:
```json
{
  "total": 3,
  "results": [
    {
      "url": "https://google.com",
      "prediction": "LEGITIMATE",
      "confidence": 0.95,
      "confidence_percentage": 95.0,
      "models": { ... },
      "features": { ... },
      "top_features": [ ... ]
    },
    {
      "url": "https://suspicious-site.com",
      "prediction": "PHISHING",
      "confidence": 0.87,
      "confidence_percentage": 87.0,
      "models": { ... },
      "features": { ... },
      "top_features": [ ... ]
    },
    {
      "url": "https://amazon.com",
      "prediction": "LEGITIMATE",
      "confidence": 0.92,
      "confidence_percentage": 92.0,
      "models": { ... },
      "features": { ... },
      "top_features": [ ... ]
    }
  ]
}
```

**Status Codes**:
- `200`: Successfully predicted all URLs
- `400`: Invalid input (empty list, > 100 URLs, or non-array format)
- `500`: Models not loaded

**Example**:
```bash
curl -X POST http://localhost:5000/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["google.com", "phishing.com", "github.com"]
  }'
```

**Note**: Batch processing is sequential but efficient for analyzing multiple URLs.

---

### 4. Feature Extraction

**Endpoint**: `POST /api/features`

**Description**: Extract heuristic features from a URL without making a prediction.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "url": "https://example.com"
}
```

**Response**:
```json
{
  "url": "https://example.com",
  "features": {
    "url_length": 20,
    "has_ip": 0,
    "domain_length": 11,
    "subdomain_count": 1,
    "has_suspicious_chars": 0,
    "special_chars_in_domain": 0,
    "url_entropy": 3.45,
    "double_slash_in_path": 0,
    "has_https": 1,
    "query_length": 0,
    "has_query_string": 0,
    "equals_in_url": 0,
    "at_symbol": 0,
    "dots_in_domain": 1,
    "hyphens_in_domain": 0,
    "percent_sign": 0,
    "valid_tld": 1,
    "short_domain_high_entropy": 0,
    "has_port": 0,
    "has_redirect": 0,
    "digits_in_domain": 0,
    "domain_mixed_suspicious": 0
  },
  "feature_names": [
    "url_length",
    "has_ip",
    "domain_length",
    ...
  ]
}
```

**Status Codes**:
- `200`: Features extracted successfully
- `400`: Invalid URL or missing field

**Example**:
```bash
curl -X POST http://localhost:5000/api/features \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-banking.com/verify"}'
```

**Use Case**: When you want to understand what features the model is analyzing for a particular URL.

---

### 5. Model Statistics

**Endpoint**: `GET /api/stats`

**Description**: Get information about trained models and available features.

**Response**:
```json
{
  "models": {
    "random_forest": {
      "type": "Random Forest Classifier",
      "n_estimators": 100,
      "max_depth": 20
    },
    "svm": {
      "type": "Support Vector Machine",
      "kernel": "rbf"
    }
  },
  "features": {
    "total_features": 22,
    "feature_names": [
      "url_length",
      "has_ip",
      "domain_length",
      "subdomain_count",
      "has_suspicious_chars",
      ...
    ]
  },
  "ensemble_method": "Average probability of RF and SVM"
}
```

**Status Codes**:
- `200`: Statistics retrieved successfully

**Example**:
```bash
curl http://localhost:5000/api/stats
```

---

## Error Handling

### Error Response Format
```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Error Cases

#### Missing Required Field
**Status**: 400
```json
{
  "error": "Missing \"url\" in request body"
}
```

#### Invalid URL
**Status**: 400
```json
{
  "error": "Error analyzing URL: [details]"
}
```

#### URL Too Long
**Status**: 400
```json
{
  "error": "URL too long (max 2048 chars)"
}
```

#### Models Not Loaded
**Status**: 500
```json
{
  "error": "Models not loaded"
}
```

#### Invalid Input Format
**Status**: 400
```json
{
  "error": "\"urls\" must be a list"
}
```

#### Too Many URLs
**Status**: 400
```json
{
  "error": "Maximum 100 URLs per request"
}
```

---

## Rate Limiting & Constraints

| Constraint | Value |
|-----------|-------|
| Max URL length | 2048 characters |
| Max URLs per batch | 100 |
| Request timeout | 10 seconds |
| Max URLs per request | 100 |

---

## Examples

### Example 1: Check a Single URL

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://gmail.com"}'
```

**Expected Response**:
```json
{
  "url": "https://gmail.com",
  "prediction": "LEGITIMATE",
  "confidence": 0.96,
  "confidence_percentage": 96.0,
  ...
}
```

### Example 2: Batch Check Multiple URLs

```bash
curl -X POST http://localhost:5000/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "google.com",
      "facebook.com",
      "phishing-bank-verify.com"
    ]
  }'
```

### Example 3: Python Client

```python
import requests
import json

API_URL = 'http://localhost:5000/api'

# Single prediction
response = requests.post(
    f'{API_URL}/predict',
    json={'url': 'https://example.com'}
)
result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence_percentage']}%")

# Batch prediction
response = requests.post(
    f'{API_URL}/predict-batch',
    json={'urls': ['google.com', 'phishing.com']}
)
results = response.json()
for pred in results['results']:
    print(f"{pred['url']}: {pred['prediction']}")
```

### Example 4: JavaScript Client

```javascript
async function scanUrl(url) {
  const response = await fetch('http://localhost:5000/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: url })
  });
  
  const result = await response.json();
  console.log(`URL: ${result.url}`);
  console.log(`Prediction: ${result.prediction}`);
  console.log(`Confidence: ${result.confidence_percentage}%`);
}

scanUrl('https://example.com');
```

---

## CORS Support

The API supports CORS requests from any origin. You can safely call the API from web applications.

**CORS Headers**:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Performance Notes

- Single URL prediction: ~100-500ms
- Batch prediction (10 URLs): ~1-5 seconds
- Batch prediction (100 URLs): ~10-50 seconds

Performance depends on:
- Machine specifications
- Network latency (for redirect checking)
- URL complexity

---

## Troubleshooting

### "Models not loaded" Error
**Cause**: Models haven't been trained yet
**Solution**: Run `python train_models.py`

### Connection Refused
**Cause**: Flask API not running
**Solution**: Start API with `python src/app.py`

### Timeout on Batch Request
**Cause**: Processing too many URLs
**Solution**: Reduce batch size or increase timeout

---

## Future Enhancements

- API key authentication
- Rate limiting
- Caching layer
- WebSocket support for real-time scanning
- Webhook support for automated scanning
- Database integration for URL history

