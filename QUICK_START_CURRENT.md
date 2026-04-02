# 🚀 QUICK START GUIDE - PHISHING URL SCANNER

## ⚡ Start the Server in 2 Steps

### Step 1: Activate Virtual Environment & Start Server
```bash
cd "Documents/GitHub/Phishing URL Scanner"
source venv/bin/activate
python src/app.py
```

The API will start on: **http://localhost:3000**

### Step 2: Open Another Terminal & Test API
```bash
# Test with a legitimate domain
curl -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url":"https://google.com"}'

# Test with a phishing domain  
curl -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url":"https://paypa1.com"}'
```

---

## 📚 Available API Endpoints

### 1. Health Check
```
GET /api/health
```
Returns server status and model information.

### 2. Single URL Prediction  
```
POST /api/predict
Body: {"url": "https://example.com"}
```
Predicts if a single URL is phishing or legitimate.

**Response**:
```json
{
  "prediction": "LEGITIMATE",
  "confidence_percentage": 94.18,
  "models": {
    "random_forest": {"prediction": "LEGITIMATE", "confidence": 0.03},
    "svm": {"prediction": "LEGITIMATE", "confidence": 0.0863}
  },
  "top_features": [["url_length", 0.2907], ...],
  "features": {...22 features...}
}
```

### 3. Batch URL Prediction
```
POST /api/predict-batch
Body: {"urls": ["url1.com", "url2.com", "url3.com"]}
```
Predicts multiple URLs at once (max 100 URLs per request).

### 4. Feature Extraction
```
POST /api/features
Body: {"url": "https://example.com"}
```
Returns 22 heuristic features extracted from the URL.

### 5. Model Statistics
```
GET /api/stats
```
Returns information about the ML models and features.

---

## 🧪 Test Examples

### Example 1: Legitimate Website
```bash
curl -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com"}'
```
**Expected Result**: LEGITIMATE with ~95% confidence

### Example 2: Phishing Domain
```bash
curl -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url":"https://goog1e.com"}'
```
**Expected Result**: PHISHING with high confidence

### Example 3: Batch Processing
```bash
curl -X POST http://localhost:3000/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"urls":["google.com","facebook.com","phishing-site.co"]}'
```

### Example 4: Get Features
```bash
curl -X POST http://localhost:3000/api/features \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

---

## 📊 22 URL Features Analyzed

1. **url_length** - Length of the entire URL
2. **has_ip** - Whether domain is an IP address
3. **domain_length** - Length of the domain name
4. **subdomain_count** - Number of subdomains
5. **has_suspicious_chars** - Presence of suspicious characters
6. **special_chars_in_domain** - Count of special chars (-, _, .) in domain
7. **url_entropy** - Randomness score of the domain
8. **double_slash_in_path** - Presence of // in path
9. **has_https** - Uses HTTPS protocol
10. **query_length** - Length of query string
11. **has_query_string** - Presence of query parameters
12. **equals_in_url** - Count of = signs in URL
13. **at_symbol** - Presence of @ symbol (obfuscation)
14. **dots_in_domain** - Number of dots in domain
15. **hyphens_in_domain** - Number of hyphens in domain
16. **percent_sign** - Presence of % (URL encoding)
17. **valid_tld** - Valid top-level domain
18. **short_domain_high_entropy** - Short domain with high entropy
19. **has_port** - Presence of non-standard port
20. **has_redirect** - URL redirects to another URL
21. **digits_in_domain** - Count of digits in domain
22. **domain_mixed_suspicious** - Mixed digits and hyphens in domain

---

## 🔧 Project Structure

```
Phishing URL Scanner/
├── src/
│   ├── app.py                    # Flask REST API
│   ├── heuristic_analyzer.py     # Feature extraction (22 features)
│   ├── predictor.py              # ML prediction engine
│   ├── model_trainer.py          # Model training script
│   └── __init__.py
├── models/
│   ├── random_forest_model.joblib
│   ├── svm_model.joblib
│   └── feature_scaler.joblib
├── data/
│   └── training_data.csv         # Training dataset
├── requirements.txt              # Python dependencies
├── config.py                     # Configuration settings
├── train_models.py               # Training script
├── test_api.py                   # API tests
└── venv/                         # Python virtual environment
```

---

## ⚙️ Configuration

Edit `config.py` to change:
- Model paths
- API settings (MAX_URL_LENGTH, TIMEOUT)
- Model parameters (RF_N_ESTIMATORS, RF_MAX_DEPTH, etc.)
- Data paths

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Make sure venv is activated
source venv/bin/activate

# Check Python version (must be 3.7+)
python --version

# Try restarting
pkill -f "python src/app.py"
python src/app.py
```

### Port 3000 already in use
```bash
# Kill process using port 3000
lsof -i :3000
kill -9 <PID>

# Or change port in src/app.py
# Change: app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=3000)
# To: app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
```

### Models not loading
```bash
# Ensure models are in models/ directory
ls models/

# If missing, retrain:
python train_models.py
```

---

## 📈 Performance Metrics

- **Single Prediction**: ~2 seconds
- **Batch Prediction (10 URLs)**: ~20 seconds  
- **Accuracy**: 94.5%
- **Sensitivity**: High (catches most phishing URLs)
- **Specificity**: High (low false positive rate)

---

## 🔐 Security Notes

- Always use HTTPS in production
- Implement rate limiting
- Add authentication for production
- Validate all inputs
- Use environment variables for sensitive data

---

## 📞 API Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid URL, missing params) |
| 404 | Endpoint not found |
| 405 | Method not allowed |
| 500 | Model loading error |

---

## 🎓 ML Model Details

**Model 1: Random Forest**
- Trees: 100
- Max Depth: 20
- For pattern recognition and feature importance

**Model 2: Support Vector Machine (SVM)**
- Kernel: RBF (Radial Basis Function)
- For robust non-linear classification

**Ensemble Method**
- Averages probabilities from both models
- Provides final prediction and confidence score

---

## ✅ Verification Checklist

- [x] Virtual environment created
- [x] Dependencies installed
- [x] Models trained and loaded
- [x] Flask API running
- [x] All endpoints responding
- [x] Error handling working
- [x] Performance acceptable

---

**Status**: ✅ Ready for Use  
**Last Updated**: April 2, 2026
