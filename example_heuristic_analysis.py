"""
Simple Example Usage - Demonstrates core functionality
"""
import sys
sys.path.insert(0, '/Users/ziauddin/Phishing URL Scanner')

from src.heuristic_analyzer import URLHeuristicAnalyzer

def main():
    print("\n" + "="*70)
    print("PHISHING URL SCANNER - EXAMPLE: HEURISTIC ANALYSIS")
    print("="*70)
    
    analyzer = URLHeuristicAnalyzer()
    
    # Example URLs to analyze
    test_urls = [
        ('https://google.com', 'LEGITIMATE'),
        ('https://am4zon.com', 'PHISHING'),
        ('http://194.168.5.5/bank/admin', 'PHISHING'),
        ('https://github.com', 'LEGITIMATE'),
        ('https://paypa1-verify.com', 'PHISHING'),
    ]
    
    for url, expected_type in test_urls:
        print(f"\n\nAnalyzing: {url}")
        print(f"Expected: {expected_type}")
        print("-" * 70)
        
        features = analyzer.analyze_url(url)
        
        # Display key suspicious features
        print("\nKey Features Extracted:")
        
        suspicious_indicators = {
            'has_ip': features.get('has_ip', 0),
            'url_length': features.get('url_length', 0),
            'subdomain_count': features.get('subdomain_count', 0),
            'special_chars_in_domain': features.get('special_chars_in_domain', 0),
            'url_entropy': features.get('url_entropy', 0),
            'has_https': features.get('has_https', 0),
            'at_symbol': features.get('at_symbol', 0),
        }
        
        for feature_name, value in suspicious_indicators.items():
            print(f"  • {feature_name:30} : {value}")
        
        # Calculate suspicious score based on heuristics
        suspicious_score = 0
        if features.get('has_ip'):
            suspicious_score += 3
        if features.get('subdomain_count', 0) > 2:
            suspicious_score += 2
        if features.get('special_chars_in_domain', 0) > 2:
            suspicious_score += 2
        if features.get('url_entropy', 0) > 4:
            suspicious_score += 2
        if features.get('at_symbol'):
            suspicious_score += 3
        if not features.get('has_https'):
            suspicious_score += 1
        
        print(f"\nHeuristic Suspicious Score: {suspicious_score}/13")
        
        if suspicious_score >= 5:
            heuristic_prediction = "⚠️  LIKELY PHISHING"
        else:
            heuristic_prediction = "✅ LIKELY LEGITIMATE"
        
        print(f"Heuristic Prediction: {heuristic_prediction}")

if __name__ == '__main__':
    main()
