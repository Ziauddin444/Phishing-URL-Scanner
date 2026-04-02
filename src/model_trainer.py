"""
ML Model Training Module
Trains Random Forest and SVM models on phishing URL dataset
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from src.heuristic_analyzer import URLHeuristicAnalyzer

class ModelTrainer:
    """Trains and evaluates phishing detection models"""
    
    def __init__(self, config=Config):
        self.config = config
        self.analyzer = URLHeuristicAnalyzer()
        self.models = {}
        self.scaler = StandardScaler()
        self.feature_names = self.analyzer.get_feature_names()
        
    def prepare_dataset(self, urls_legitimate, urls_phishing):
        """
        Create training dataset from legitimate and phishing URLs
        urls_legitimate: list of legitimate URLs
        urls_phishing: list of phishing URLs
        """
        print("Preparing training dataset...")
        
        # Extract features from all URLs
        X = []
        y = []
        
        for url in urls_legitimate:
            try:
                features = self.analyzer.analyze_url(url)
                X.append([features[name] for name in self.feature_names])
                y.append(0)  # 0 = legitimate
            except:
                pass
        
        for url in urls_phishing:
            try:
                features = self.analyzer.analyze_url(url)
                X.append([features[name] for name in self.feature_names])
                y.append(1)  # 1 = phishing
            except:
                pass
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"Dataset prepared: {len(X)} URLs, {len(self.feature_names)} features")
        print(f"Legitimate URLs: {sum(y == 0)}, Phishing URLs: {sum(y == 1)}")
        
        return X, y
    
    def train_models(self, X, y):
        """Train both Random Forest and SVM models"""
        
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.config.TEST_SIZE,
            random_state=self.config.RANDOM_STATE,
            stratify=y
        )
        
        # Scale features for SVM
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("\n" + "="*50)
        print("TRAINING RANDOM FOREST MODEL")
        print("="*50)
        
        # Train Random Forest
        rf_model = RandomForestClassifier(
            n_estimators=self.config.RF_N_ESTIMATORS,
            max_depth=self.config.RF_MAX_DEPTH,
            random_state=self.config.RANDOM_STATE,
            n_jobs=-1
        )
        rf_model.fit(X_train, y_train)
        
        # Evaluate Random Forest
        y_pred_rf = rf_model.predict(X_test)
        rf_accuracy = accuracy_score(y_test, y_pred_rf)
        rf_precision = precision_score(y_test, y_pred_rf)
        rf_recall = recall_score(y_test, y_pred_rf)
        rf_f1 = f1_score(y_test, y_pred_rf)
        
        print(f"Random Forest Accuracy:  {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
        print(f"Random Forest Precision: {rf_precision:.4f}")
        print(f"Random Forest Recall:    {rf_recall:.4f}")
        print(f"Random Forest F1-Score:  {rf_f1:.4f}")
        
        print("\n" + "="*50)
        print("TRAINING SVM MODEL")
        print("="*50)
        
        # Train SVM
        svm_model = SVC(
            kernel=self.config.SVM_KERNEL,
            probability=True,
            random_state=self.config.RANDOM_STATE
        )
        svm_model.fit(X_train_scaled, y_train)
        
        # Evaluate SVM
        y_pred_svm = svm_model.predict(X_test_scaled)
        svm_accuracy = accuracy_score(y_test, y_pred_svm)
        svm_precision = precision_score(y_test, y_pred_svm)
        svm_recall = recall_score(y_test, y_pred_svm)
        svm_f1 = f1_score(y_test, y_pred_svm)
        
        print(f"SVM Accuracy:  {svm_accuracy:.4f} ({svm_accuracy*100:.2f}%)")
        print(f"SVM Precision: {svm_precision:.4f}")
        print(f"SVM Recall:    {svm_recall:.4f}")
        print(f"SVM F1-Score:  {svm_f1:.4f}")
        
        # Ensemble accuracy (average of both models)
        y_pred_ensemble = ((rf_model.predict_proba(X_test)[:, 1] + 
                           svm_model.predict_proba(X_test_scaled)[:, 1]) / 2 > 0.5).astype(int)
        ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)
        
        print("\n" + "="*50)
        print("ENSEMBLE MODEL (Average Probability)")
        print("="*50)
        print(f"Ensemble Accuracy: {ensemble_accuracy:.4f} ({ensemble_accuracy*100:.2f}%)")
        
        self.models['random_forest'] = rf_model
        self.models['svm'] = svm_model
        
        return {
            'rf': {'model': rf_model, 'accuracy': rf_accuracy},
            'svm': {'model': svm_model, 'accuracy': svm_accuracy},
            'scaler': self.scaler
        }
    
    def save_models(self, models_dict):
        """Save trained models to disk"""
        os.makedirs(self.config.MODEL_DIR, exist_ok=True)
        
        joblib.dump(models_dict['rf']['model'], self.config.RANDOM_FOREST_MODEL)
        joblib.dump(models_dict['svm']['model'], self.config.SVM_MODEL)
        joblib.dump(models_dict['scaler'], self.config.SCALER_MODEL)
        
        print(f"\nModels saved:")
        print(f"  - Random Forest: {self.config.RANDOM_FOREST_MODEL}")
        print(f"  - SVM: {self.config.SVM_MODEL}")
        print(f"  - Scaler: {self.config.SCALER_MODEL}")
    
    def load_models(self):
        """Load pre-trained models from disk"""
        self.models['random_forest'] = joblib.load(self.config.RANDOM_FOREST_MODEL)
        self.models['svm'] = joblib.load(self.config.SVM_MODEL)
        self.scaler = joblib.load(self.config.SCALER_MODEL)
        return self.models
