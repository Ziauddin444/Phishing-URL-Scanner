# 🎯 PHISHING URL SCANNER - COMPLETE EXECUTION GUIDE

Welcome! This guide shows you **exactly how to run the entire project** in simple steps.

---

## ⚡ FASTEST WAY (5 clicks)

### Option A: Interactive Runner (Recommended for Beginners)

```bash
cd "Phishing URL Scanner"
python runner.py
```

Then choose:
- **Option 1** → Setup & Train
- **Option 3** → Start API
- **Open new terminal** → Option 4 → Test API

### Option B: Bash Script (Best for Automation)

```bash
cd "Phishing URL Scanner"
bash quick_start.sh        # Sets up and trains
python src/app.py          # Starts API
```

---

## 📖 COMPLETE STEP-BY-STEP GUIDE

### Prerequisites ✓
- macOS with zsh (or Linux/Windows)
- Python 3.7+
- Internet connection

### Step 1: Navigate to Project

```bash
cd "Phishing URL Scanner"
```

You should see this structure:
```
├── src/
├── models/
├── data/
├── COMMANDS.txt
├── train_models.py
├── test_api.py
└── runner.py
```

---

### Step 2: Create Virtual Environment (First Time Only)

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

**Windows Users:**
```cmd
python -m venv venv
venv\Scripts\activate
```

---

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify:**
```bash
python3 -c "import flask, sklearn; print('✅ All good!')"
```

---

### Step 4: Train ML Models

```bash
python train_models.py
```

**You should see:**
```
==================================================
TRAINING RANDOM FOREST MODEL
==================================================
Random Forest Accuracy:  0.80-0.95 (80-95%)
Random Forest Precision: 0.75+
Random Forest Recall:    0.75+
Random Forest F1-Score:  0.75+

==================================================
TRAINING SVM MODEL
==================================================
SVM Accuracy:  0.80-0.95 (80-95%)
SVM Precision: 0.75+
SVM Recall:    0.75+
SVM F1-Score:  0.75+

==================================================
ENSEMBLE MODEL
==================================================
Ensemble Accuracy: 0.80-0.95 (80-95%)

Models saved:
  - models/random_forest_model.joblib ✓
  - models/svm_model.joblib ✓
  - models/feature_scaler.joblib ✓
```

⏱️ **Takes 1-3 minutes**

---

### Step 5: Start the API Server

**IMPORTANT: Keep this terminal open!**

```bash
python src/app.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * Press CTRL+C to quit
```

🎉 **API is now LIVE!**

---

### Step 6: Test the API (NEW TERMINAL)

**Open a NEW terminal window and run:**

```bash
cd "Phishing URL Scanner"
source venv/bin/activate
python test_api.py
```

**You should see test results:**
```
TEST 1: Health Check
{'status': 'healthy', 'service': 'Phishing URL Scanner', 'version': '1.0.0', 'models_loaded': True}

TEST 2: Single URL Prediction
URL: https://google.com
Prediction: LEGITIMATE
Confidence: 95.23%
...
```

---

## 🛠️ QUICK REFERENCE COMMANDS

### After First Setup, Subsequent Runs:

```bash
# Terminal 1: Start API
cd "Phishing URL Scanner"
source venv/bin/activate
python src/app.py

# Terminal 2: Test API
cd "Phishing URL Scanner"
source venv/bin/activate
python test_api.py
```

### Retrain Models (If you update training data):

```bash
source venv/bin/activate
python train_models.py
```

### Manual API Testing with CURL:

```bash
# Health check
curl http://localhost:5000/api/health

# Test single URL
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'

# Test batch URLs
curl -X POST http://localhost:5000/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://google.com", "https://am4zon.com"]}'

# Get model stats
curl http://localhost:5000/api/stats
```

---

## ✅ SUCCESS CHECKLIST

| Step | Check | Status |
|------|-------|--------|
| 1 | Virtual environment created | ✓ (venv) shows in terminal |
| 2 | Dependencies installed | ✓ No error messages |
| 3 | Models trained | ✓ 3 .joblib files in models/ |
| 4 | API running | ✓ "Running on http://127.0.0.1:5000" |
| 5 | Health check works | ✓ curl returns {"status": "healthy"} |
| 6 | Predictions work | ✓ curl returns prediction results |
| 7 | All tests pass | ✓ test_api.py shows all PASS |

---

## 🚨 TROUBLESHOOTING

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install dependencies again
```bash
pip install -r requirements.txt
```

### Problem: "Models not found" when starting API
**Solution:** Train models first
```bash
python train_models.py
```

### Problem: "Port 5000 is already in use"
**Solution A:** Kill the old process
```bash
lsof -i :5000
kill -9 <PID>
```

**Solution B:** Use different port (edit src/app.py)
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```
Then test on: `http://localhost:5001`

### Problem: "venv: command not found"
**Solution:** Activate the virtual environment
```bash
source venv/bin/activate
```

### Problem: Tests fail with connection error
**Solution:** Make sure API is running in another terminal
- Terminal 1: `python src/app.py` (MUST be running)
- Terminal 2: `python test_api.py` (for testing)

---

## 📊 WHAT HAPPENS IN EACH STEP

| Step | Does What | Output |
|------|-----------|--------|
| Train Models | Trains 2 ML models on 54 sample URLs | 3 model files (.joblib) |
| Start API | Runs Flask web server | http://localhost:5000 |
| Test API | Makes HTTP requests to API | Test results (PASS/FAIL) |
| Health Check | Verifies API is running | {"status": "healthy"} |
| Prediction | Analyzes URL with ML models | Phishing or Legitimate + confidence% |

---

## 🔄 TYPICAL WORKFLOW

```
First Time:
├─ Step 1: python3 -m venv venv
├─ Step 2: source venv/bin/activate
├─ Step 3: pip install -r requirements.txt
├─ Step 4: python train_models.py
├─ Step 5: python src/app.py (Terminal 1)
└─ Step 6: python test_api.py (Terminal 2)

Subsequent Times:
├─ Terminal 1: source venv/bin/activate → python src/app.py
└─ Terminal 2: source venv/bin/activate → python test_api.py
```

---

## 🎯 NEXT STEPS AFTER SUCCESS

### 1. **Use the API in Python Code**
```python
import requests

response = requests.post(
    'http://localhost:5000/api/predict',
    json={'url': 'https://example.com'}
)
result = response.json()
print(f"URL: {result['url']}")
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence_percentage']}%")
```

### 2. **Improve the Model**
- Add more URLs to `data/training_data.csv`
- Run `python train_models.py` again
- Models automatically retrain with new data

### 3. **Deploy to Production**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
```

### 4. **Integrate with Frontend**
- API accepts POST requests
- Returns JSON responses
- Use any frontend framework (React, Vue, etc.)

---

## 📚 ADDITIONAL RESOURCES

| Document | Purpose |
|----------|---------|
| `COMMANDS.txt` | All available commands |
| `GETTING_STARTED.md` | Detailed architecture guide |
| `API_DOCUMENTATION.md` | API endpoint reference |
| `README.md` | Project overview |
| `RUN_GUIDE.md` | Running guide (alternative) |

---

## ✨ QUICK COMMAND SUMMARY

```bash
# One-liner for first-time setup and run
cd "Phishing URL Scanner" && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python train_models.py

# One-liner for starting API
python src/app.py

# One-liner for testing (new terminal)
source venv/bin/activate && python test_api.py
```

---

## 📞 NEED HELP?

1. Check section **🚨 TROUBLESHOOTING** above
2. Read `GETTING_STARTED.md` for detailed explanations
3. Check `API_DOCUMENTATION.md` for endpoint details
4. Review `PROJECT_SUMMARY.md` for architecture overview

---

**You're all set! 🎉 Happy phishing detection!**

**Current Date:** February 1, 2026
**Last Updated:** 2026-02-01
**Status:** ✅ Ready to Run
