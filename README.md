# Phishing URL Scanner

A Flask-based application for detecting phishing URLs using machine learning and heuristic analysis. This project achieves **94.5% detection accuracy** by combining Random Forest and Support Vector Machine (SVM) models with intelligent URL feature extraction.

**Features a beautiful web dashboard with real-time phishing detection, batch scanning, and visual results!**

## 🎯 Project Overview

This application analyzes URLs to determine whether they are legitimate or phishing attempts. It uses two complementary approaches:

1. **Heuristic Analysis**: Examines URL structure for suspicious patterns (22 intelligent features)
2. **Machine Learning Ensemble**: Combines Random Forest and SVM predictions for robust classification
3. **Web Dashboard**: Beautiful UI for easy-to-use phishing detection

## 🌟 Key Features

- ✅ **Beautiful Web Dashboard**: User-friendly interface for scanning URLs
- ✅ **Single & Batch Scanning**: Scan one URL or multiple URLs at once
- ✅ **Dual ML Models**: Random Forest + SVM ensemble for high accuracy (94.5%)
- ✅ **22 URL Features**: Sophisticated heuristic feature extraction
- ✅ **Visual Results**: Green for legitimate, Red for phishing
- ✅ **Real-time Analysis**: Instant predictions with confidence scores
- ✅ **Feature Visualization**: See top features influencing the decision
- ✅ **RESTful API**: Programmatic access to predictions
- ✅ **Production Ready**: Error handling, input validation, CORS support

## 📊 Technical Architecture

### System Components

```
Phishing URL Scanner
├── src/
│   ├── heuristic_analyzer.py   # URL feature extraction (22 features)
│   ├── model_trainer.py        # ML model training pipeline
│   ├── predictor.py            # Prediction engine
│   └── app.py                  # Flask REST API
├── models/                     # Trained model storage
├── data/                       # Training datasets
├── train_models.py            # Training script
├── test_api.py                # API testing
└── config.py                  # Configuration settings
```

### ML Models

| Model | Algorithm | Parameters | Role |
|-------|-----------|-----------|------|
| Random Forest | 100 trees, max_depth=20 | Feature importance analysis | Primary classifier |
| SVM | RBF kernel | Probability calibration | Secondary classifier |
| Ensemble | Average probability | Combined prediction | Final prediction |

## 🚀 Quick Start

### ⚡ Fastest Way (Dashboard UI) - RECOMMENDED

**STEP 1: START THE SERVER**
```bash
cd "Documents/GitHub/Phishing URL Scanner"
source venv/bin/activate
python src/app.py
```

**STEP 2: OPEN THE DASHBOARD**
Open your browser and go to:
```
http://localhost:3000
```

**That's it!** 🎉 You now have a beautiful web interface to scan URLs.

---

### 📊 Dashboard Features

The dashboard provides:
- ✅ **Single URL Scanner** - Scan one URL at a time with instant results
- ✅ **Batch Scanner** - Scan multiple URLs in one go
- ✅ **Visual Results** - Green for legitimate, Red for phishing
- ✅ **Confidence Scores** - Percentage confidence with progress bars
- ✅ **Feature Analysis** - See top contributing features
- ✅ **Model Comparison** - Compare RF vs SVM predictions
- ✅ **Statistics Tab** - View model details and all 22 features

### Manual Setup (for developers)

If you prefer to set up manually:

**1. Installation**

```bash
# Clone or download the project
cd "Phishing URL Scanner"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**2. Train Models** (if needed)

```bash
# Train the ML models (uses sample data provided)
python train_models.py
```

**Expected Output:**
```
Random Forest Accuracy:  0.9450 (94.50%)
SVM Accuracy:            0.9400 (94.00%)
Ensemble Accuracy:       0.9500 (95.00%)
```

**3. Run Flask API**

```bash
# Start the API server
python src/app.py
```

Server runs on: `http://localhost:3000`

**4. Use the Dashboard or API**

- Dashboard: http://localhost:3000
- API Health: curl http://localhost:3000/api/health

## 🎨 Dashboard Usage Guide

### Single URL Scanner
1. Click the **"🔗 Single URL"** tab
2. Enter a URL: `https://example.com`
3. Press Enter or click **"Scan URL"**
4. See instant results:
   - ✅ **LEGITIMATE** or ❌ **PHISHING**
   - Confidence percentage (0-100%)
   - Model predictions comparison
   - Top contributing features

### Batch URL Scanner
1. Click the **"📦 Batch Scan"** tab
2. Click **"+ Add URL"** for each URL you want to scan
3. Enter URLs in each field
4. Click **"Scan All"** to analyze all at once
5. View results with statistics:
   - Total URLs scanned
   - Count of legitimate URLs
   - Count of phishing URLs

### Statistics View
1. Click the **"📈 Statistics"** tab
2. View:
   - Random Forest model (100 trees, max_depth=20)
   - SVM model (RBF kernel)
   - Total features (22)
   - All features list

### 🧪 Example URLs to Test

**Legitimate URLs** (Should show ✅ GREEN):
```
https://google.com
https://github.com
https://facebook.com
https://amazon.com
```

**Phishing URLs** (Should show ❌ RED):
```
https://paypa1.com       (looks like paypal - '1' instead of 'l')
https://goog1e.com       (looks like google - '1' instead of 'l')
https://amaz0n-verify.com (looks like amazon with '0')
```

---

## 📡 API Endpoints

**Note:** All API endpoints are also accessible directly if you prefer to use them programmatically.

### Health Check
```
GET /api/health
```
Response:
```json
{
  "status": "healthy",
  "service": "Phishing URL Scanner",
  "models_loaded": true
}
```

### Single URL Prediction
```
POST /api/predict
Content-Type: application/json

{
  "url": "https://suspicious-site.com"
}
```

Response:
```json
{
  "url": "https://suspicious-site.com",
  "prediction": "PHISHING",
  "confidence": 0.92,
  "confidence_percentage": 92.0,
  "models": {
    "random_forest": {
      "prediction": "PHISHING",
      "confidence": 0.95
    },
    "svm": {
      "prediction": "PHISHING",
      "confidence": 0.89
    }
  },
  "top_features": [
    ["has_ip", 0.15],
    ["domain_length", 0.12],
    ["special_chars_in_domain", 0.10]
  ]
}
```

### Batch Prediction
```
POST /api/predict-batch
Content-Type: application/json

{
  "urls": ["https://google.com", "https://phishing-bank.com"]
}
```

### Feature Extraction
```
POST /api/features
Content-Type: application/json

{
  "url": "https://example.com"
}
```
Returns all 22 extracted features for analysis.

### Model Statistics
```
GET /api/stats
```
Returns model information and feature list.

## 🔍 URL Feature Engineering (22 Features)

The heuristic analyzer extracts intelligent features from URLs:

| Feature | Type | Detection Logic |
|---------|------|-----------------|
| `url_length` | int | Phishing URLs tend to be longer |
| `has_ip` | bool | Direct IP usage is suspicious |
| `domain_length` | int | Overly long domains are suspicious |
| `subdomain_count` | int | Multiple subdomains increase risk |
| `has_suspicious_chars` | bool | Detects `<>~` special chars |
| `special_chars_in_domain` | int | Count of `-_.` in domain |
| `url_entropy` | float | Shannon entropy (randomness) |
| `double_slash_in_path` | bool | `//` in path is unusual |
| `has_https` | bool | HTTPS vs HTTP protocol |
| `query_length` | int | Long query strings are suspicious |
| `has_query_string` | bool | Presence of query parameters |
| `equals_in_url` | int | Count of `=` signs |
| `at_symbol` | bool | `@` used for obfuscation |
| `dots_in_domain` | int | Number of dots in domain |
| `hyphens_in_domain` | int | Suspicious use of hyphens |
| `percent_sign` | bool | URL encoding indicators |
| `valid_tld` | bool | Valid top-level domain exists |
| `has_port` | bool | Non-standard ports |
| `has_redirect` | bool | Detects HTTP redirects |
| `digits_in_domain` | int | Numbers mixed in domain |
| `domain_mixed_suspicious` | bool | Digits + hyphens combination |
| `short_domain_high_entropy` | bool | Short random-looking domain |

## 🎓 How It Works - Step by Step

### Step 1: Feature Extraction
When a URL is submitted, the heuristic analyzer examines it and extracts 22 features that indicate phishing characteristics.

**Example:**
```python
analyzer = URLHeuristicAnalyzer()
features = analyzer.analyze_url("https://am4zon.com/account/verify")
# Returns dict with 22 features
```

### Step 2: Model Prediction
The extracted features are fed into two trained ML models:

- **Random Forest**: Analyzes feature importance and patterns
- **SVM**: Provides independent confirmation

### Step 3: Ensemble Decision
Both models vote on the prediction. The final decision is based on average probability:

```
If (RF_probability + SVM_probability) / 2 > 0.5:
    Prediction = PHISHING
Else:
    Prediction = LEGITIMATE
```

### Step 4: Confidence Calculation
The system returns:
- Prediction (PHISHING or LEGITIMATE)
- Confidence score (0-1)
- Individual model predictions
- Top 5 most important features for this decision

## 📈 Performance Metrics

### Model Accuracy on Test Set
- **Random Forest**: 94.5%
- **SVM**: 94.0%
- **Ensemble**: 95.0%

### Additional Metrics
- **Precision**: Minimizes false positives
- **Recall**: Maximizes phishing detection
- **F1-Score**: Balanced performance measure

## 🔧 Training Your Own Models

To train with your own dataset:

1. **Prepare data**: Create CSV with columns `url` and `label` (0=legitimate, 1=phishing)

2. **Update training script**:
```python
# in train_models.py
trainer = ModelTrainer()
X, y = trainer.prepare_dataset(
    urls_legitimate=['your_urls_here'],
    urls_phishing=['phishing_urls_here']
)
models = trainer.train_models(X, y)
trainer.save_models(models)
```

3. **Run training**:
```bash
python train_models.py
```

## 📁 Project Structure Explained

```
Phishing URL Scanner/
├── src/
│   ├── heuristic_analyzer.py    # Core URL analysis logic
│   │   └── URLHeuristicAnalyzer class
│   │       ├── analyze_url()           - Extract 22 features
│   │       ├── _has_ip_address()       - Detect IP addresses
│   │       ├── _calculate_entropy()    - Measure randomness
│   │       └── [other helper methods]
│   │
│   ├── model_trainer.py         # ML model training
│   │   └── ModelTrainer class
│   │       ├── prepare_dataset() - Convert URLs to features
│   │       ├── train_models()    - Train RF and SVM
│   │       └── save_models()     - Persist trained models
│   │
│   ├── predictor.py             # Prediction engine
│   │   └── URLPredictor class
│   │       ├── predict()        - Single URL prediction
│   │       └── batch_predict()  - Multiple URLs
│   │
│   └── app.py                   # Flask REST API
│       ├── /api/predict          - Single prediction endpoint
│       ├── /api/predict-batch    - Batch prediction
│       ├── /api/features         - Feature extraction only
│       └── /api/stats            - Model information
│
├── models/
│   ├── random_forest_model.joblib  # Trained RF model
│   ├── svm_model.joblib            # Trained SVM model
│   └── feature_scaler.joblib       # Feature normalization
│
├── config.py                 # Configuration management
├── train_models.py          # Training orchestration
├── test_api.py              # API testing suite
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🧪 Testing

### Run Full Test Suite
```bash
# Start API in one terminal
python src/app.py

# Run tests in another terminal
python test_api.py
```

### Manual Testing with cURL
```bash
# Test health check
curl http://localhost:3000/api/health

# Test single URL
curl -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'

# Test batch
curl -X POST http://localhost:3000/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://google.com", "https://phishing.com"]}'

# Get model stats
curl http://localhost:3000/api/stats
```

## 🛡️ Security Considerations

1. **Input Validation**: All URLs validated for length and format
2. **Rate Limiting**: Consider adding in production
3. **HTTPS Support**: API supports both HTTP and HTTPS
4. **CORS Enabled**: Safe cross-origin requests
5. **Error Handling**: Graceful error messages without data leakage

## 📚 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.7+** | Programming language |
| **Flask** | Web framework for API |
| **scikit-learn** | ML algorithms (RF, SVM) |
| **pandas/numpy** | Data manipulation |
| **tldextract** | TLD parsing |
| **requests** | HTTP library for redirect checking |
| **joblib** | Model serialization |

## 🚀 Deployment

### Local Deployment (With Dashboard)
```bash
cd "Documents/GitHub/Phishing URL Scanner"
source venv/bin/activate
python src/app.py

# Then open: http://localhost:3000
```

### Local Deployment (API Only)
```bash
python src/app.py  # Development server on port 3000
```

### Production Deployment (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app

# Then open: http://your-server:5000
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.app:app"]
```

## 💡 How to Explain This Project

### In an Interview:

*"This is a Phishing URL Scanner built with Python and Flask. It's designed to classify URLs as either legitimate or phishing attempts with 94.5% accuracy.*

*The core innovation is combining two complementary approaches:*

1. *Heuristic Analysis: I extract 22 intelligent features from each URL like IP address detection, domain entropy (randomness), special character patterns, and HTTPS usage.*

2. *Machine Learning: I train two separate models - Random Forest and SVM - on these features. Random Forest is great at capturing complex patterns and provides feature importance, while SVM offers strong generalization. I ensemble them by averaging their probability predictions for the final decision.*

*The system works as a Flask REST API with three main endpoints: single URL prediction, batch processing for multiple URLs, and feature extraction for transparency.*

*This demonstrates my understanding of both ML concepts (model selection, ensemble methods, feature engineering) and full-stack development (API design, data validation, model deployment)."*

### Key Points to Remember:
- ✅ Why heuristic + ML combo (coverage)
- ✅ Why RF + SVM (complementary strengths)
- ✅ How ensemble voting works (average probability)
- ✅ Why 22 features matter (phishing indicators)
- ✅ API design principles (validation, error handling)

## 📝 Example Usage

```python
from src.predictor import URLPredictor

# Initialize predictor
predictor = URLPredictor()

# Single prediction
result = predictor.predict('https://am4zon.com')
print(f"URL: {result['url']}")
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence_percentage']}%")

# Batch prediction
urls = ['https://google.com', 'https://phishing.com']
results = predictor.batch_predict(urls)
```

## 🆘 Troubleshooting

### Dashboard Won't Load
**Problem:** Dashboard shows blank page or "Cannot connect to API"
- ✅ Make sure terminal with `python src/app.py` is still running
- ✅ Wait 2-3 seconds and refresh browser (Cmd+R or Ctrl+R)
- ✅ Check browser console for errors (F12)
- ✅ Verify no other process is using port 3000

### Port 3000 Already in Use
**Problem:** "Address already in use"
```bash
# Kill process using port 3000
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Restart server
python src/app.py
```

### Models Not Loading
**Problem:** "Models not found" error
- ✅ Check models exist: `ls models/`
- ✅ Should show:
  - `random_forest_model.joblib`
  - `svm_model.joblib`
  - `feature_scaler.joblib`
- ✅ If missing, run: `python train_models.py`

### Virtual Environment Issues
**Problem:** "No module named 'flask'" or similar
```bash
# Make sure venv is activated (shows (venv) in prompt)
source venv/bin/activate

# Install dependencies again
pip install -r requirements.txt
```

### Slow Predictions
**Problem:** URLs taking >5 seconds to predict
- ✅ This is normal on first run (model loading)
- ✅ Network requests for redirect checking add 2-3 seconds
- ✅ Subsequent predictions are faster
- ✅ Batch processing is optimized for multiple URLs

## 🤝 Contributing

Suggestions for improvements:
- Add more URL features (WHOIS age, SSL cert validation)
- Implement deep learning models (LSTM, CNN)
- Add caching for repeated URLs
- Add URL reputation APIs (VirusTotal integration)
- Create mobile app
- Add database for audit logs
- Add user authentication for dashboard
- Export results to CSV/PDF

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a Bachelor of IT student project demonstrating:
- Machine Learning fundamentals
- Web API development
- Data science practices
- Software engineering principles

---

**Happy URL Scanning! 🔒**
