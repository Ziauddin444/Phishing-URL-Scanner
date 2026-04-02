# 🚀 HOW TO RUN THE DASHBOARD

## ✅ SIMPLE 3-STEP SETUP

### **Step 1: Open Terminal and Navigate to Project**
```bash
cd "Documents/GitHub/Phishing URL Scanner"
```

### **Step 2: Activate Virtual Environment & Start Server**
```bash
source venv/bin/activate
python src/app.py
```

You should see:
```
 * Running on http://0.0.0.0:3000
 * Running on http://127.0.0.1:3000
```

### **Step 3: Open Dashboard in Browser**
```
http://localhost:3000
```

---

## 🎨 **DASHBOARD FEATURES**

### **Tab 1: 🔗 Single URL Scanner**
1. Type a URL in the input box
2. Click "Scan URL" or press Enter
3. See results instantly:
   - ✅ **LEGITIMATE** or ❌ **PHISHING**
   - 📊 Confidence percentage
   - 🤖 Model predictions (RF + SVM)
   - 🔍 Top features

**Try These:**
- `https://google.com` → Should be LEGITIMATE
- `https://paypa1.com` → Should be PHISHING
- `https://github.com` → Should be LEGITIMATE

### **Tab 2: 📦 Batch Scanner**
1. Click "+ Add URL" to add URL fields
2. Enter multiple URLs
3. Click "Scan All"
4. See results with statistics:
   - Total URLs scanned
   - Count of legitimate URLs
   - Count of phishing URLs

### **Tab 3: 📈 Statistics**
View:
- ✅ Model information (Random Forest, SVM)
- ✅ Total features (22)
- ✅ All features list
- ✅ Ensemble method details

---

## 🔧 **TROUBLESHOOTING**

### **Issue: "Cannot connect to API"**
**Solution:**
Make sure you ran both commands:
```bash
source venv/bin/activate    # This activates the environment
python src/app.py           # This starts the server
```

### **Issue: "Port 3000 already in use"**
**Solution:**
```bash
# Kill the process using port 3000
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Then restart
python src/app.py
```

### **Issue: "Empty page / not loading"**
**Solution:**
1. Wait 2-3 seconds after starting the server
2. Refresh the page (Cmd+R on Mac)
3. Check browser console (right-click → Inspect)

### **Issue: Models not loaded**
Make sure models exist in `models/` folder:
```bash
ls models/
# Should show:
# random_forest_model.joblib
# svm_model.joblib
# feature_scaler.joblib
```

If missing, train models:
```bash
python train_models.py
```

---

## 📱 **WHAT YOU CAN DO**

✅ Scan single URLs instantly  
✅ Scan multiple URLs in batch  
✅ See AI explanations of why URL is flagged  
✅ View model confidence scores  
✅ Analyze URL features  
✅ Compare two ML models (RF vs SVM)  
✅ Mobile friendly interface  

---

## 🎯 **EXAMPLE WORKFLOW**

**1. Start in Terminal 1:**
```bash
cd "Documents/GitHub/Phishing URL Scanner"
source venv/bin/activate
python src/app.py
```

**2. Open in Browser:**
```
http://localhost:3000
```

**3. Test Single URL:**
- Enter: `https://google.com`
- Click: "Scan URL"
- Result: ✅ LEGITIMATE (94.18% confidence)

**4. Test Batch:**
- Click: "+ Add URL"
- Enter URLs:
  - `https://github.com`
  - `https://facebook.com`
  - `https://phishing-site.net`
- Click: "Scan All"
- Result: See all results with stats

---

## ⚙️ **KEYBOARD SHORTCUTS**

| Action | Shortcut |
|--------|----------|
| Scan URL | Press Enter in URL field |
| Clear Result | Click "Clear" button |
| Add URL (Batch) | Click "+ Add URL" |
| Remove URL (Batch) | Click "Remove" button |

---

## 📊 **UNDERSTANDING RESULTS**

### **LEGITIMATE (Green) ✅**
- URL passes safety checks
- Low phishing score
- Trust indicators present:
  - HTTPS protocol
  - Valid domain
  - No suspicious patterns

### **PHISHING (Red) ❌**
- URL fails safety checks
- High phishing score
- Warning signs:
  - Similar to known domains (typosquatting)
  - IP address instead of domain
  - Suspicious characters
  - High entropy domain

---

## 💡 **TIPS**

1. **Test different variations:**
   - `google.com` vs `goog1e.com` (the 1 vs l)
   - `paypal.com` vs `paypa1.com` (the 1 vs l)

2. **Check the features:**
   - See which features flagged the URL
   - Understand the decision-making process

3. **Batch scanning:**
   - Great for testing multiple URLs at once
   - Useful for security checks

---

## 🆘 **STILL NOT WORKING?**

**Check these:**
1. Server running in Terminal? → Look for "Running on http://0.0.0.0:3000"
2. Browser showing blank page? → Wait 2s, then refresh
3. Getting errors? → Check browser console (F12)
4. Models missing? → Run `python train_models.py`

---

**Happy Scanning!** 🔍✨

For more help, check the terminal output for error messages.
