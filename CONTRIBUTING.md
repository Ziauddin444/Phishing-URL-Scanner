# Contributing to Phishing URL Scanner

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🚀 Getting Started

### 1. Fork the Repository
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/phishing-url-scanner.git
cd phishing-url-scanner
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env
```

### 3. Install Pre-commit Hooks (Optional)
```bash
pip install pre-commit
pre-commit install
```

## 📋 Development Workflow

### Creating a Branch
```bash
# Create a new branch for your feature
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### Naming Conventions
- **Features**: `feature/add-whois-analysis`
- **Bug Fixes**: `fix/model-accuracy-issue`
- **Improvements**: `improvement/optimize-batch-processing`
- **Documentation**: `docs/update-readme`

### Making Changes

1. **Write clean code** following Python PEP 8 standards
2. **Add docstrings** to functions and classes
3. **Write tests** for new features
4. **Update documentation** if needed

### Code Style Guidelines

```python
# Use type hints
def predict(self, url: str) -> dict:
    """
    Predict if URL is phishing or legitimate.
    
    Args:
        url: The URL to analyze
        
    Returns:
        dict: Prediction result with confidence
    """
    pass

# Use meaningful variable names
legitimate_count = sum(1 for r in results if r['prediction'] == 'LEGITIMATE')

# Add comments for complex logic
# Calculate Shannon entropy to measure domain randomness
entropy = -sum((p := count / len(text)) * math.log2(p) for count in freq.values())
```

## 🧪 Testing

### Run Existing Tests
```bash
# Start the API server
python src/app.py

# In another terminal, run tests
python run_tests.py

# Or use pytest if you add tests
pytest tests/
```

### Write New Tests
```python
import unittest

class TestURLPredictor(unittest.TestCase):
    def setUp(self):
        from src.predictor import URLPredictor
        self.predictor = URLPredictor()
    
    def test_legitimate_url(self):
        result = self.predictor.predict('https://google.com')
        self.assertEqual(result['prediction'], 'LEGITIMATE')
    
    def test_phishing_url(self):
        result = self.predictor.predict('https://paypa1.com')
        self.assertEqual(result['prediction'], 'PHISHING')

if __name__ == '__main__':
    unittest.main()
```

## 📝 Commit Messages

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Add WHOIS age feature for phishing detection"
git commit -m "Fix timeout issue in redirect checker"

# Avoid
git commit -m "fixed stuff"
git commit -m "updates"
```

## 🔒 Security Guidelines

### Never Commit:
- ✗ API keys or tokens
- ✗ Database credentials
- ✗ Private keys or certificates
- ✗ Secrets or passwords
- ✗ `.env` files (only `.env.example` is committed)

### Environment Variables
All sensitive data should be in `.env`:
```bash
# .env (not committed)
SECRET_KEY=your-actual-secret-key
SOME_API_KEY=your-api-key

# .env.example (committed - shows structure only)
SECRET_KEY=change-me-in-production
SOME_API_KEY=your-api-key-here
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Add more URL features (WHOIS info, SSL certificate validation)
- [ ] Implement deep learning models (LSTM, CNN)
- [ ] Add URL reputation API integration (VirusTotal)
- [ ] Create mobile app

### Medium Priority
- [ ] Add database for prediction history
- [ ] Implement user authentication
- [ ] Add export to CSV/PDF
- [ ] Performance optimization
- [ ] Comprehensive test suite

### Low Priority
- [ ] Documentation improvements
- [ ] UI/UX enhancements
- [ ] Additional language support
- [ ] Docker image optimization

## 📤 Submitting Changes

### 1. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 2. Create a Pull Request
- Go to GitHub and click "Compare & pull request"
- Add a clear title and description
- Link any related issues

### 3. PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How did you test this?

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] No new warnings generated
- [ ] Tests pass
- [ ] No sensitive data in commits
```

## 🎓 Project Architecture

### To Understand the Code:

1. **src/heuristic_analyzer.py** - URL feature extraction
2. **src/predictor.py** - ML prediction logic
3. **src/model_trainer.py** - Model training pipeline
4. **src/app.py** - Flask API endpoints
5. **dashboard.html** - Web UI

### Data Flow
```
URL Input → Heuristic Analysis (22 features) → 
RF Model ┐
         ├→ Ensemble Voting → Prediction
SVM Model┘
```

## 🐛 Reporting Bugs

### Create an Issue with:
- Clear title
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error logs if available

```markdown
### Bug: Dashboard crashes on batch scan
**Environment:**
- Python 3.9
- macOS 12.6

**Steps to Reproduce:**
1. Go to dashboard
2. Add 5 URLs to batch scan
3. Click "Scan All"

**Expected:**
All URLs should be scanned and results displayed

**Actual:**
Page crashes with error: [paste error]
```

## 💬 Communication

- **Discussions**: Use GitHub Discussions for ideas
- **Issues**: Use Issues for bugs and features
- **PRs**: Use Pull Requests for code changes
- **Documentation**: Update README and docstrings

## ✅ Checklist Before Submitting PR

- [ ] Code follows project style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests written and pass
- [ ] No debug code left in
- [ ] No sensitive data committed
- [ ] Changes are focused on one thing
- [ ] Commit messages are clear
- [ ] PR description is complete

## 📚 Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Git Workflow](https://git-scm.com/book/en/v2)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🙏 Thank You!

We appreciate your contributions to making Phishing URL Scanner better!

---

**Questions?** Open an issue or discussion on GitHub.

**License**: This project is open source. By contributing, you agree to have your work licensed under the same license as the project.
