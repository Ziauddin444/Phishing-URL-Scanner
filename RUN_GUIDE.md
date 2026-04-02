# 🚀 Run Project - Quick Guide

This guide shows you how to run each stage of the Phishing URL Scanner project.

## ⚡ Super Quick Start (Copy & Paste)

```bash
# 1. Navigate to project
cd "Phishing URL Scanner"

# 2. Setup and train (automated)
bash quick_start.sh

# 3. In same terminal, start API
python src/app.py

# 4. In NEW terminal:
cd "Phishing URL Scanner"
source venv/bin/activate
python test_api.py
```

---

## 📋 Step-by-Step Guide

### Step 1️⃣: First Time Setup (5 minutes)

**Create and activate virtual environment:**

```bash
cd "Phishing URL Scanner"
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

**Install dependencies:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Verify installation:

```bash
python3 -c "import flask, sklearn; print('✅ Ready!')"
```

---

### Step 2️⃣: Train ML Models (2-3 minutes)

Make sure venv is activated, then:

```bash
python train_models.py
```

**Expected Output:**
```
==================================================
TRAINING RANDOM FOREST MODEL
==================================================
Random Forest Accuracy:  0.8000+ (80%+ accuracy)
Random Forest Precision: 0.7500+
Random Forest Recall:    0.7500+
Random Forest F1-Score:  0.7500+

==================================================
TRAINING SVM MODEL
==================================================
SVM Accuracy:  0.8000+ (80%+ accuracy)
SVM Precision: 0.7500+
SVM Recall:    0.7500+
SVM F1-Score:  0.7500+

==================================================
ENSEMBLE MODEL (Average Probability)
==================================================
Ensemble Accuracy: 0.8000+ (80%+ accuracy)

Models saved:
  - models/random_forest_model.joblib ✓
  - models/svm_model.joblib ✓
  - models/feature_scaler.joblib ✓
```

**What this does:**
- Loads sample URLs (26 phishing, 28 legitimate)
- Extracts 22 features from each URL
- Trains Random Forest (100 trees, max_depth=20)
- Trains SVM (RBF kernel)
- Evaluates both models
- Creates ensemble prediction
- Saves models to `models/` folder

---

### Step 3️⃣: Start API Server (Keep running)

```bash
python src/app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * Use a debugger or production WSGI server to run the code under HTTPS
 * Press CTRL+C to quit
```

**Don't close this terminal!** The API must keep running while you test.

---

### Step 4️⃣: Test the API (Open NEW Terminal)

In a **NEW** terminal window:

```bash
cd "Phishing URL Scanner"
source venv/bin/activate
```

**Option A: Automatic Tests (Recommended)**

```bash
python test_api.py
```

This runs all tests automatically and shows results.

**Option B: Manual CURL Tests**

```bash
# Test 1: Health Check
curl http://localhost:5000/api/health

# Test 2: Check a legitimate URL
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'

# Test 3: Check a suspicious URL
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://am4zon.com"}'

# Test 4: Check multiple URLs
curl -X POST http://localhost:5000/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://google.com", "https://github.com", "https://am4zon.com"]}'

# Test 5: See URL features
curl -X POST http://localhost:5000/api/features \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Test 6: Get model stats
curl http://localhost:5000/api/stats
```

---

## 🎯 Running the Full Workflow

```bash
# Terminal 1: Setup and Train
cd "Phishing URL Scanner"
source venv/bin/activate
python train_models.py

# Same terminal: Start API
python src/app.py
# → API now running on http://localhost:5000

---

# Terminal 2: Test
cd "Phishing URL Scanner"
source venv/bin/activate
python test_api.py
# → See test results
```

---

## ✅ Success Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed without errors
- [ ] Training completed (models saved)
- [ ] API server running on port 5000
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Predictions work for legitimate URLs
- [ ] Predictions work for suspicious URLs
- [ ] Batch predictions work
- [ ] Feature extraction works

---

## 🔧 Troubleshooting

### "Models not found" Error
**Solution:** Make sure you ran `python train_models.py` first

### "Port 5000 already in use"
**Solution:** Kill the old process:
```bash
lsof -i :5000
kill -9 <PID>
```

Or change port in `src/app.py` (line ~195):
```python
app.run(debug=True, port=5001)  # Use 5001 instead
```

### "venv: command not found"
**Solution:** Activate virtual environment:
```bash
source venv/bin/activate
```

### "No module named flask"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
Phishing URL Scanner/
├── src/
│   ├── app.py              # Flask API server
│   ├── heuristic_analyzer.py  # URL feature extraction
│   ├── model_trainer.py    # Training pipeline
│   └── predictor.py        # Prediction engine
├── models/                 # Trained models (created by train_models.py)
│   ├── random_forest_model.joblib
│   ├── svm_model.joblib
│   └── feature_scaler.joblib
├── data/
│   └── training_data.csv   # Sample training data
├── train_models.py         # Run this to train models
├── test_api.py             # Run this to test API
├── config.py               # Configuration settings
└── COMMANDS.txt            # All available commands
```

---

## 🚀 Next Steps After Testing

1. **Deploy the API:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
   ```

2. **Use in Python Code:**
   ```python
   import requests
   response = requests.post('http://localhost:5000/api/predict',
                           json={'url': 'https://example.com'})
   print(response.json())
   ```

3. **Train with Your Own Data:**
   - Add URLs to `data/training_data.csv`
   - Run `python train_models.py` again
   - Models will retrain automatically

4. **Monitor and Improve:**
   - Collect predictions from production
   - Identify misclassified URLs
   - Retrain with better examples

---

## 📖 More Information

- **All Commands:** See `COMMANDS.txt`
- **Detailed Guide:** See `GETTING_STARTED.md`
- **API Docs:** See `API_DOCUMENTATION.md`
- **Project Summary:** See `PROJECT_SUMMARY.md`

---

**Happy analyzing! 🎉**
