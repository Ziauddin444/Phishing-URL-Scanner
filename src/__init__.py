"""
Phishing URL Scanner - Python Package
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "ML-based Phishing URL Detection System"

from src.heuristic_analyzer import URLHeuristicAnalyzer
from src.predictor import URLPredictor
from src.model_trainer import ModelTrainer

__all__ = ['URLHeuristicAnalyzer', 'URLPredictor', 'ModelTrainer']
