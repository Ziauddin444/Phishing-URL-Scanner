"""
Flask REST API for Phishing URL Scanner
Provides endpoints for URL prediction and batch scanning
"""
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import sys
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config, config, ProductionConfig
from src.predictor import URLPredictor
from src.heuristic_analyzer import URLHeuristicAnalyzer

# Configure logging (never use print() in production)
logging.basicConfig(
    level=getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper(), logging.INFO),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# ---------------------------------------------------------------------------
# CORS — hardened: read allowed origins from environment variable so no
# secrets are ever hardcoded and the policy is easy to tighten in production.
# Alert #8 fix: allow_private_network=False (disabled by default in 6.x)
# ---------------------------------------------------------------------------
_raw_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '*')
allowed_origins = [o.strip() for o in _raw_origins.split(',') if o.strip()]
CORS(
    app,
    origins=allowed_origins,
    supports_credentials=False,   # must be False when origins='*'
)

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

# Log configuration — use logger, never print()
logger.info("Loaded config: %s (DEBUG=%s)", env, app.config['DEBUG'])

# ---------------------------------------------------------------------------
# Security headers — applied to every response via after_request hook
# ---------------------------------------------------------------------------
@app.after_request
def set_security_headers(response):
    """Attach hardened HTTP security headers to every outgoing response."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    # Restrict CSP; loosen only if you serve embedded assets
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    )
    # Only send HSTS when actually running over HTTPS
    if request.is_secure or os.environ.get('FLASK_ENV') == 'production':
        response.headers['Strict-Transport-Security'] = (
            'max-age=31536000; includeSubDomains; preload'
        )
    # Remove server fingerprinting header
    response.headers.pop('Server', None)
    return response

# Initialize predictor with Config class, not Flask config
try:
    predictor = URLPredictor(config_class)
except Exception as e:
    logger.warning("Models not loaded. Train models first. Error: %s", e)
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
def _validate_json_field(data, field_name, required=True):
    """DRY: Validate JSON request fields"""
    if not data:
        return None, error_response(f'Invalid JSON body', 400)
    if field_name not in data:
        return None, error_response(f'Missing "{field_name}" in request body', 400)
    return data[field_name], None

def _normalize_url(url):
    """DRY: Add protocol and clean URLs"""
    if isinstance(url, str):
        url = url.strip()
    if not url:
        return None
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

@app.route('/api/predict', methods=['POST'])
def predict_url():
    """
    Predict if a single URL is phishing or legitimate
    
    POST /api/predict
    {"url": "https://example.com"}
    """
    if not predictor:
        return error_response('Models not loaded', 500)
    
    url, err = _validate_json_field(request.get_json(), 'url')
    if err:
        return err
    
    url = _normalize_url(url)
    if not url:
        return error_response('URL cannot be empty', 400)
    
    if len(url) > app.config['MAX_URL_LENGTH']:
        return error_response(f'URL too long (max {app.config["MAX_URL_LENGTH"]} chars)', 400)
    
    try:
        result = predictor.predict(url)
        return jsonify(result), 200
    except ValueError as e:
        logger.warning("Prediction ValueError for url=%s: %s", url, e)
        return error_response(str(e), 400)
    except Exception as e:
        logger.error("Unexpected prediction error: %s", e, exc_info=True)
        # Never expose raw exception messages to API consumers
        return error_response('An error occurred processing the URL', 500)

# ============= BATCH PREDICTION =============
@app.route('/api/predict-batch', methods=['POST'])
def predict_batch():
    """
    Predict multiple URLs at once
    
    POST /api/predict-batch
    {"urls": ["url1.com", "url2.com"]}
    """
    if not predictor:
        return error_response('Models not loaded', 500)
    
    urls, err = _validate_json_field(request.get_json(), 'urls')
    if err:
        return err
    
    if not isinstance(urls, list):
        return error_response('"urls" must be a list', 400)
    
    if len(urls) == 0:
        return error_response('URLs list cannot be empty', 400)
    
    if len(urls) > 100:
        return error_response('Maximum 100 URLs per request', 400)
    
    # Normalize all URLs (DRY principle)
    urls = [_normalize_url(url) for url in urls]
    
    try:
        results = predictor.batch_predict(urls)
        return jsonify({
            'total': len(results),
            'results': results
        }), 200
    except ValueError as e:
        logger.warning("Batch prediction ValueError: %s", e)
        return error_response(str(e), 400)
    except Exception as e:
        logger.error("Unexpected batch prediction error: %s", e, exc_info=True)
        return error_response('An error occurred processing the URLs', 500)

# ============= FEATURE EXTRACTION ONLY =============
@app.route('/api/features', methods=['POST'])
def extract_features():
    """
    Extract heuristic features from a URL without prediction
    
    POST /api/features
    {"url": "https://example.com"}
    """
    url, err = _validate_json_field(request.get_json(), 'url')
    if err:
        return err
    
    url = _normalize_url(url)
    if not url:
        return error_response('URL cannot be empty', 400)
    
    try:
        features = analyzer.analyze_url(url)
        return jsonify({
            'url': url,
            'features': features,
            'feature_names': analyzer.get_feature_names()
        }), 200
    except Exception as e:
        logger.error("Feature extraction error: %s", e, exc_info=True)
        return error_response('An error occurred extracting features', 500)

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

# ============= UTILITY FUNCTIONS =============
def error_response(message, status_code):
    """DRY: Create consistent error responses"""
    return jsonify({'error': message}), status_code

# ============= ERROR HANDLERS =============
_ERROR_HANDLERS = {
    404: ('Endpoint not found', 404),
    500: ('Internal server error', 500),
    405: ('Method not allowed', 405),
}

for error_code, (message, status_code) in _ERROR_HANDLERS.items():
    @app.errorhandler(error_code)
    def handle_error(error, msg=message, code=status_code):
        return error_response(msg, code)

if __name__ == '__main__':
    # Development only — in production use gunicorn:
    # gunicorn "src.app:app" -b 0.0.0.0:3000 --workers 4
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=3000)
