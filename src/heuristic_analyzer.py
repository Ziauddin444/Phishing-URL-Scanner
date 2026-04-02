"""
URL Heuristic Analysis Module
Extracts features from URLs to detect phishing characteristics
"""
import re
from urllib.parse import urlparse, parse_qs
import requests
import tldextract
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

class URLHeuristicAnalyzer:
    """
    Analyzes URLs and extracts heuristic features
    These features are used for ML model prediction
    """
    
    def __init__(self, timeout=3):
        self.timeout = timeout
        
    def analyze_url(self, url):
        """
        Extract all heuristic features from a URL
        Returns: dict with 20+ features for ML model
        """
        features = {}
        
        try:
            # Parse URL
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path
            
            # Feature 1: URL Length
            features['url_length'] = len(url)
            
            # Feature 2: Has IP Address
            features['has_ip'] = self._has_ip_address(domain)
            
            # Feature 3: Domain Length
            features['domain_length'] = len(domain)
            
            # Feature 4: Subdomain Count
            features['subdomain_count'] = self._count_subdomains(domain)
            
            # Feature 5: Has Suspicious Characters
            features['has_suspicious_chars'] = self._has_suspicious_characters(url)
            
            # Feature 6: Special Chars in Domain
            features['special_chars_in_domain'] = self._count_special_chars(domain)
            
            # Feature 7: URL Entropy (randomness in domain)
            features['url_entropy'] = self._calculate_entropy(domain)
            
            # Feature 8: Double Slash in Path
            features['double_slash_in_path'] = 1 if '//' in path else 0
            
            # Feature 9: Using HTTPS
            features['has_https'] = 1 if parsed.scheme == 'https' else 0
            
            # Feature 10: Query String Chars
            query = parsed.query
            features['query_length'] = len(query)
            
            # Feature 11: Has Query String
            features['has_query_string'] = 1 if query else 0
            
            # Feature 12: Equals Signs in URL (common in phishing)
            features['equals_in_url'] = url.count('=')
            
            # Feature 13: At Symbol in URL (used for obfuscation)
            features['at_symbol'] = 1 if '@' in url else 0
            
            # Feature 14: Number of Dots in Domain
            features['dots_in_domain'] = domain.count('.')
            
            # Feature 15: Number of Hyphens in Domain
            features['hyphens_in_domain'] = domain.count('-')
            
            # Feature 16: Percent Sign (URL encoding)
            features['percent_sign'] = 1 if '%' in url else 0
            
            # Feature 17: TLD Analysis
            ext = tldextract.extract(url)
            features['valid_tld'] = 1 if ext.suffix else 0
            
            # Feature 18: Short Domain with High Entropy (suspicious)
            features['short_domain_high_entropy'] = 1 if (
                len(domain) < 15 and features['url_entropy'] > 4
            ) else 0
            
            # Feature 19: Port in URL
            features['has_port'] = 1 if ':' in domain and parsed.port else 0
            
            # Feature 20: Redirects (try to fetch)
            features['has_redirect'] = self._check_for_redirect(url)
            
            # Feature 21: Digits in Domain
            features['digits_in_domain'] = sum(1 for c in domain if c.isdigit())
            
            # Feature 22: Domain has numbers and hyphens (common in phishing)
            features['domain_mixed_suspicious'] = 1 if (
                features['digits_in_domain'] > 0 and features['hyphens_in_domain'] > 0
            ) else 0
            
        except Exception as e:
            print(f"Error analyzing URL: {e}")
            # Return default features with 0 if error occurs
            features = {f: 0 for f in range(1, 23)}
        
        return features
    
    def _has_ip_address(self, domain):
        """Check if domain is actually an IP address"""
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'
        return 1 if re.match(ip_pattern, domain.split(':')[0]) else 0
    
    def _count_subdomains(self, domain):
        """Count number of subdomains"""
        # Remove port if present
        domain = domain.split(':')[0]
        # Count dots = number of domain levels - 1
        return domain.count('.')
    
    def _has_suspicious_characters(self, url):
        """Check for suspicious characters like < > ~ ` etc"""
        suspicious = set('<>~`^[]{}|\\')
        return 1 if any(char in url for char in suspicious) else 0
    
    def _count_special_chars(self, domain):
        """Count special characters in domain"""
        special = set('-_.')
        return sum(1 for char in domain if char in special)
    
    def _calculate_entropy(self, text):
        """
        Calculate Shannon entropy of text
        Higher entropy = more random = suspicious
        """
        import math
        if len(text) == 0:
            return 0
        
        # Calculate frequency of each character
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0
        for count in freq.values():
            p = count / len(text)
            entropy -= p * math.log2(p)
        
        return round(entropy, 2)
    
    def _check_for_redirect(self, url):
        """Check if URL redirects (returns different URL)"""
        try:
            # Skip network checks for URLs that don't start with http
            if not url.startswith(('http://', 'https://')):
                return 0
            
            response = requests.head(
                url, 
                timeout=self.timeout, 
                allow_redirects=False,
                verify=False
            )
            return 1 if response.status_code in [301, 302, 303, 307, 308] else 0
        except (requests.Timeout, requests.ConnectionError, requests.RequestException, Exception):
            # On timeout or connection error, default to 0 (no redirect detected)
            return 0
    
    def get_feature_names(self):
        """Return list of feature names in order"""
        return [
            'url_length', 'has_ip', 'domain_length', 'subdomain_count',
            'has_suspicious_chars', 'special_chars_in_domain', 'url_entropy',
            'double_slash_in_path', 'has_https', 'query_length',
            'has_query_string', 'equals_in_url', 'at_symbol',
            'dots_in_domain', 'hyphens_in_domain', 'percent_sign',
            'valid_tld', 'short_domain_high_entropy', 'has_port',
            'has_redirect', 'digits_in_domain', 'domain_mixed_suspicious'
        ]
