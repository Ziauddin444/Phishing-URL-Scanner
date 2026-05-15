"""
Flask REST API for Phishing URL Scanner
Provides endpoints for URL prediction and batch scanning
"""
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config, config, ProductionConfig
from src.predictor import URLPredictor
from src.heuristic_analyzer import URLHeuristicAnalyzer

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load config - DEFAULT TO PRODUCTION SAFETY
env = os.environ.get('FLASK_ENV', 'production')
if env not in config:
    print(f"Warning: Unknown FLASK_ENV '{env}', using production config")
    env = 'production'
config_class = config.get(env, ProductionConfig)

# SECURITY: Ensure DEBUG is never True in production
if env == 'production' and config_class.DEBUG:
    print("ERROR: DEBUG must be False in production!")
    config_class.DEBUG = False

# Apply config to Flask app
app.config.from_object(config_class)

# Log configuration
print(f"Loaded config: {env} (DEBUG={app.config['DEBUG']})")

# Initialize predictor with Config class, not Flask config
try:
    predictor = URLPredictor(config_class)
except Exception as e:
    print(f"Warning: Models not loaded. Train models first. Error: {e}")
    predictor = None

analyzer = URLHeuristicAnalyzer()

# ============= DASHBOARD =============
@app.route('/', methods=['GET'])
def dashboard():
    """Serve the dashboard"""
    dashboard_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dashboard.html')
    if os.path.exists(dashboard_path):
        return send_file(dashboard_path)
    return jsonify({'error': 'Dashboard not found'}), 404

# ============= HEALTH CHECK =============
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Phishing URL Scanner',
        'version': '1.0.0',
        'models_loaded': predictor is not None
    })

# ============= SINGLE URL PREDICTION =============
@app.route('/api/predict', methods=['POST'])
def predict_url():
    """
    Predict if a single URL is phishing or legitimate
    
    POST /api/predict
    {
        "url": "https://example.com"
    }
    """
    if not predictor:
        return jsonify({'error': 'Models not loaded'}), 500
    
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing "url" in request body'}), 400
    
    url = data['url'].strip()
    
    if not url:
        return jsonify({'error': 'URL cannot be empty'}), 400
    
    if len(url) > app.config['MAX_URL_LENGTH']:
        return jsonify({'error': f'URL too long (max {app.config["MAX_URL_LENGTH"]} chars)'}), 400
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        result = predictor.predict(url)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============= BATCH PREDICTION =============
@app.route('/api/predict-batch', methods=['POST'])
def predict_batch():
    """
    Predict multiple URLs at once
    
    POST /api/predict-batch
    {
        "urls": ["url1.com", "url2.com"]
    }
    """
    if not predictor:
        return jsonify({'error': 'Models not loaded'}), 500
    
    data = request.get_json()
    
    if not data or 'urls' not in data:
        return jsonify({'error': 'Missing "urls" in request body'}), 400
    
    urls = data['urls']
    
    if not isinstance(urls, list):
        return jsonify({'error': '"urls" must be a list'}), 400
    
    if len(urls) == 0:
        return jsonify({'error': 'URLs list cannot be empty'}), 400
    
    if len(urls) > 100:
        return jsonify({'error': 'Maximum 100 URLs per request'}), 400
    
    # Add protocol to URLs if missing
    urls = [
        url if url.startswith(('http://', 'https://')) else 'https://' + url 
        for url in urls
    ]
    
    try:
        results = predictor.batch_predict(urls)
        return jsonify({
            'total': len(results),
            'results': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============= FEATURE EXTRACTION ONLY =============
@app.route('/api/features', methods=['POST'])
def extract_features():
    """
    Extract heuristic features from a URL without prediction
    
    POST /api/features
    {
        "url": "https://example.com"
    }
    """
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing "url" in request body'}), 400
    
    url = data['url'].strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        features = analyzer.analyze_url(url)
        return jsonify({
            'url': url,
            'features': features,
            'feature_names': analyzer.get_feature_names()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============= MODEL STATISTICS =============
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get model statistics and information"""
    return jsonify({
        'models': {
            'random_forest': {
                'type': 'Random Forest Classifier',
                'n_estimators': 100,
                'max_depth': 20
            },
            'svm': {
                'type': 'Support Vector Machine',
                'kernel': 'rbf'
            }
        },
        'features': {
            'total_features': len(analyzer.get_feature_names()),
            'feature_names': analyzer.get_feature_names()
        },
        'ensemble_method': 'Average probability of RF and SVM'
    }), 200

# ============= ERROR HANDLERS =============
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=3000)
