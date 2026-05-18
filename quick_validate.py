#!/usr/bin/env python3
"""Quick validation - Test basic imports and configuration"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("Testing imports...")
try:
    from config import DevelopmentConfig, ProductionConfig, TestingConfig
    print("✅ Config classes imported successfully")
    print(f"  - DevelopmentConfig: DEBUG={DevelopmentConfig.DEBUG}, SECRET_KEY set={bool(DevelopmentConfig.SECRET_KEY)}")
    print(f"  - TestingConfig: DEBUG={TestingConfig.DEBUG}, SECRET_KEY set={bool(TestingConfig.SECRET_KEY)}")
except Exception as e:
    print(f"❌ Config import failed: {e}")
    sys.exit(1)

try:
    from predictor import URLPredictor
    print("✅ URLPredictor imported successfully")
except Exception as e:
    print(f"❌ URLPredictor import failed: {e}")
    sys.exit(1)

try:
    from heuristic_analyzer import URLHeuristicAnalyzer
    print("✅ URLHeuristicAnalyzer imported successfully")
except Exception as e:
    print(f"❌ URLHeuristicAnalyzer import failed: {e}")
    sys.exit(1)

try:
    analyzer = URLHeuristicAnalyzer()
    features = analyzer.analyze_url('https://google.com')
    print(f"✅ Feature extraction works: {len(features)} features")
except Exception as e:
    print(f"❌ Feature extraction failed: {e}")
    sys.exit(1)

print("\n✅ All basic validations passed!")
