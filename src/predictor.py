"""
URL Predictor Module
Uses trained models to predict if URLs are phishing or legitimate
"""
import joblib
import numpy as np
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from src.heuristic_analyzer import URLHeuristicAnalyzer

class URLPredictor:
    """Predicts if a URL is phishing or legitimate using trained models"""
    
    def __init__(self, config=Config):
        self.config = config
        self.analyzer = URLHeuristicAnalyzer()
        self.rf_model = None
        self.svm_model = None
        self.scaler = None
        self.feature_names = self.analyzer.get_feature_names()
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            self.rf_model = joblib.load(self.config.RANDOM_FOREST_MODEL)
            self.svm_model = joblib.load(self.config.SVM_MODEL)
            self.scaler = joblib.load(self.config.SCALER_MODEL)
        except FileNotFoundError:
            raise Exception("Models not found. Please train models first.")
    
    def predict(self, url):
        """
        Predict if URL is phishing or legitimate
        Returns: dict with prediction, confidence, and feature details
        """
        # Extract features
        features_dict = self.analyzer.analyze_url(url)
        X = np.array([[features_dict[name] for name in self.feature_names]])
        
        # Scale features for SVM
        X_scaled = self.scaler.transform(X)
        
        # Get predictions and probabilities
        rf_prediction = self.rf_model.predict(X)[0]
        rf_probability = self.rf_model.predict_proba(X)[0]
        
        svm_prediction = self.svm_model.predict(X_scaled)[0]
        svm_probability = self.svm_model.predict_proba(X_scaled)[0]
        
        # Ensemble prediction (average probabilities)
        ensemble_prob = (rf_probability[1] + svm_probability[1]) / 2
        ensemble_prediction = 1 if ensemble_prob > 0.5 else 0
        
        # Determine label and confidence
        if ensemble_prediction == 1:
            label = 'PHISHING'
            confidence = ensemble_prob
        else:
            label = 'LEGITIMATE'
            confidence = 1 - ensemble_prob
        
        # Get feature importance from Random Forest
        importance_scores = self.rf_model.feature_importances_
        feature_importance = list(zip(self.feature_names, importance_scores))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        top_features = feature_importance[:5]
        
        result = {
            'url': url,
            'prediction': label,
            'confidence': round(float(confidence), 4),
            'confidence_percentage': round(float(confidence) * 100, 2),
            'models': {
                'random_forest': {
                    'prediction': 'PHISHING' if rf_prediction == 1 else 'LEGITIMATE',
                    'confidence': round(float(rf_probability[1]), 4)
                },
                'svm': {
                    'prediction': 'PHISHING' if svm_prediction == 1 else 'LEGITIMATE',
                    'confidence': round(float(svm_probability[1]), 4)
                }
            },
            'features': features_dict,
            'top_features': [(name, round(score, 4)) for name, score in top_features]
        }
        
        return result
    
    def batch_predict(self, urls):
        """Predict multiple URLs at once"""
        results = []
        for url in urls:
            try:
                result = self.predict(url)
                results.append(result)
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e)
                })
        return results
