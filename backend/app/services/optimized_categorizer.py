import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

class OptimizedPerfectCategorizer:
    def __init__(self):
        self.model = None
        self.is_trained = False
        
        # Enhanced rule patterns with better accuracy
        self.rule_patterns = {
            'Food': [
                'zomato', 'swiggy', 'dominos', 'pizza', 'mcdonald', 'kfc', 'burger',
                'restaurant', 'cafe', 'food', 'biryani', 'hotel', 'canteen', 'dining',
                'thearogya', 'grandmaslil', 'asanbaibiriyani', 'kitchenking', 'frozen bottle',
                'paakashala', 'chulhachaukida', 'manjal restaurant', 'madrascoffee',
                'edenparkcafete', 'sri swapnas caf', 'sukkubhaifoodspriv', 'sukkubhaifoods'
            ],
            'Travel': [
                'redbus', 'irctc', 'uber', 'ola', 'makemytrip', 'goibibo', 'indigo',
                'spicejet', 'railway', 'flight', 'bus', 'taxi', 'metro', 'train',
                'indianrailways', 'chennaimetrorail', 'indian railways', 'confirm ticket',
                'metropolitan transpo', 'sk smart busine'
            ],
            'Bills': [
                'electricity', 'tneb', 'bescom', 'water', 'bwssb', 'gas', 'broadband',
                'wifi', 'internet', 'dth', 'tatasky', 'tataplay', 'fiber', 'airtel',
                'airtelpayments', 'airteldirectupipo', 'jio', 'myjio', 'bsnl', 'vi',
                'reliance jio', 'vishnu cars ser', 'morpheus vibaen', 'vineeth prints',
                'icicimerchantservi', 'srivinayagatrad', 'avighnaenterprises'
            ],
            'Shopping': [
                'amazon', 'flipkart', 'myntra', 'ajio', 'nykaa', 'snapdeal',
                'shopping', 'mall', 'store', 'retail', 'westside', 'reliance',
                'westsideunitof', 'reliancedigital', 'trent', 'go colors', 'gocolors',
                'decathlon', 'zudio', 'max retail', 'snitchapparels', 'greentrends',
                'magicpin', 'sri maha stores', 'sublrelements', 'wwwamazonin'
            ],
            'Entertainment': [
                'netflix', 'hotstar', 'jiohotstar', 'prime', 'bookmyshow', 'movie', 'cinema',
                'youtube', 'spotify', 'gaming', 'subscription', 'entertainment',
                'bigtree', 'my11circle', 'wwwwoohoo', 'executive lounge', 'bookmy show',
                'ebsredeemnowin', 'nagarjunaandhra', 'apdfgurucom'
            ],
            'Subscriptions': [
                'openai', 'chatgpt', 'youtube', 'netflix', 'subscription', 'premium',
                'appleservices', 'apple services'
            ],
            'Salary': [
                'salary', 'payroll', 'employee', 'credited by', 'monthly salary',
                'epsilon', 'conversant', 'epsilonindiadataa', 'conversantswdev'
            ],
            'Investments': [
                'mutual fund', 'sip', 'fd', 'nps', 'stock', 'dividend',
                'investment', 'investnow', 'investnowip', 'sspbenterprises'
            ],
            'EMI': [
                'emi', 'loan', 'installment', 'bajaj', 'repayment', 'emi466289677chqs'
            ],
            'Health': [
                'apollo', 'hospital', 'pharmacy', 'medplus', 'doctor',
                'medical', 'clinic', 'health', 'medicine', 'shreeramdev medical',
                'santhanam pharmacy', 'apollo ph'
            ],
            'Education': [
                'school', 'college', 'university', 'fees', 'tuition', 'byjus',
                'vedantu', 'coursera', 'udemy', 'education', 'anna university',
                'annauniversity', 'ccaannauniversity'
            ],
            'Bank_Charges': [
                'atm charge', 'sms fee', 'debit card fee', 'account maintenance',
                'neft charge', 'bank charge', 'markup', 'dcintlpostxnmarkup',
                'chrg', 'debit card annual fee', 'cashwdrl'
            ],
            'Groceries': [
                'bigbasket', 'grofers', 'dmart', 'grocery', 'vegetables',
                'instamart', 'blinkit', 'zepto', 'dunzo', 'amazonpay groceries',
                'zeptonow', 'zeptomarketplace', 'shopwel mart', 'easybazar',
                'cn2easybazarsupe', 'cn1easybazarsuper', 'kpnfarmfresh',
                'sri maha super', 'grace supermark', 'spar2167elemen',
                'sri maha superm', 'sri maha stores'
            ],
            'Fuel': [
                'parsons fuels', 'shreelpkpetropa', 'equitas fastag'
            ],
            'ATM': [
                'nwd', 'atw', 'atl', 'cashwdrl'
            ],
            'Interest': [
                'interestpaid', 'interest paid'
            ],
            'Rent': [
                'rent', 'rentformay'
            ]
        }
        
        # High priority patterns that override person detection
        self.priority_patterns = {
            'Food': [
                r'zomato.*', r'swiggy.*', r'dominos.*', r'pizza.*',
                r'.*cafe.*', r'.*restaurant.*', r'.*hotel.*', r'.*food.*'
            ],
            'Shopping': [
                r'amazon.*', r'magicpin.*', r'pos\d+.*amazon.*', r'pos\d+.*westside.*'
            ],
            'Entertainment': [
                r'bookmy.*show.*', r'my11circle.*', r'netflix.*'
            ],
            'Subscriptions': [
                r'openai.*chatgp.*', r'apple.*services.*'
            ],
            'Bills': [
                r'airtel.*', r'jio.*', r'tataplay.*'
            ]
        }
        
        # Person name patterns
        self.person_patterns = [
            r'\bmr\s+[a-z]+', r'\bmrs\s+[a-z]+', r'\bms\s+[a-z]+',
            r'\b[a-z]+\s+[a-z]+\s*-\s*[a-z0-9@]+',
            r'\b[a-z]{3,}\s+[a-z]{3,}(?:\s+[a-z])?$'
        ]
        
        # Person names from transaction data
        self.person_names = [
            'meenakshi', 'saiganesh', 'murugadoss', 'rizwan', 'mugesh', 'chandragiriya',
            'manikandan', 'vabhinesh', 'varun', 'kumaresan', 'rahul', 'sivaprakash',
            'balamurali', 'palakolanu', 'mudassir', 'govindagouda', 'surinenianjali',
            'mrdhanikachalam', 'rahmathulla', 'sowmiya', 'rmahesh', 'manjula',
            'bharathkumar', 'harshavardhan', 'ashanmuga', 'mrsuresh', 'sindhukumar',
            'prakash', 'thajudeen', 'mrahamed', 'gnanasekar', 'mrkrishnak', 'punith',
            'moneiruddin', 'sriram', 'rukmani', 'subasri', 'jerald', 'kamalakannan',
            'charles', 'prabhu', 'rajasekar', 'kishanth', 'mathesh', 'rajendran',
            'baskar', 'goutham', 'venkataraman', 'abbielessh', 'janardhanan',
            'balachandiran', 'noeline', 'ayyanar', 'pavithra', 'jijojonson',
            'venu', 'rakkel', 'yesur', 'miztherishi', 'jaya', 'karthikeya',
            'prdeep', 'niranjansubba', 'hegde', 'madaraje', 'ancy', 'anand'
        ]
    
    def _extract_features(self, description):
        """Enhanced feature extraction"""
        if pd.isna(description):
            return ""
        
        desc = str(description).lower().strip()
        desc = re.sub(r'\b\d{10,}\b', ' ', desc)
        desc = re.sub(r'[^\w\s@.-]', ' ', desc)
        desc = re.sub(r'\s+', ' ', desc).strip()
        
        return desc
    
    def _detect_person(self, description):
        """Enhanced person detection"""
        clean_desc = self._extract_features(description)
        
        # Check for Mr/Mrs/Ms patterns
        for pattern in self.person_patterns:
            if re.search(pattern, clean_desc):
                return True
        
        # Check for person names
        for name in self.person_names:
            if name in clean_desc:
                return True
        
        return False
    
    def _rule_classify(self, description):
        """Enhanced rule-based classification with priority handling"""
        clean_desc = self._extract_features(description)
        
        # Step 1: Check high priority patterns first (overrides person detection)
        for category, patterns in self.priority_patterns.items():
            for pattern in patterns:
                if re.search(pattern, clean_desc):
                    return category, 0.98
        
        # Step 2: Check person patterns (but not if already matched priority)
        if self._detect_person(description):
            # Double check it's not a merchant with person name
            merchant_keywords = ['cafe', 'restaurant', 'hotel', 'shop', 'store', 'mart', 'super']
            if not any(keyword in clean_desc for keyword in merchant_keywords):
                return 'Person', 0.96
        
        # Step 3: Check keyword patterns
        category_scores = {}
        for category, keywords in self.rule_patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in clean_desc:
                    score += len(keyword.split())
            
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            confidence = min(0.97, 0.85 + (category_scores[best_category] * 0.02))
            return best_category, confidence
        
        return 'Person', 0.343  # Default fallback
    
    def train(self, df):
        """Train the model with transaction data"""
        if df.empty:
            return
        
        # Prepare features
        features = df['Description'].apply(self._extract_features)
        labels = df['Category']
        
        # Create and train pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        self.model.fit(features, labels)
        self.is_trained = True
    
    def predict(self, description):
        """Predict category for a single transaction"""
        # First try rule-based classification
        rule_category, rule_confidence = self._rule_classify(description)
        
        # If high confidence rule match, return it
        if rule_confidence >= 0.95:
            return rule_category, rule_confidence
        
        # If model is trained, use it for low confidence cases
        if self.is_trained and self.model:
            try:
                features = self._extract_features(description)
                ml_category = self.model.predict([features])[0]
                ml_confidence = max(self.model.predict_proba([features])[0])
                
                # Combine rule and ML predictions
                if rule_confidence > ml_confidence:
                    return rule_category, rule_confidence
                else:
                    return ml_category, ml_confidence * 0.9
            except:
                pass
        
        return rule_category, rule_confidence
    
    def predict_batch(self, descriptions):
        """Predict categories for multiple transactions"""
        results = []
        for desc in descriptions:
            category, confidence = self.predict(desc)
            results.append((category, confidence))
        return results

# Test the categorizer
if __name__ == "__main__":
    categorizer = OptimizedPerfectCategorizer()
    
    # Test cases
    test_cases = [
        "UPI-ZOMATO LTD-ZOMATO-ORDER@PTYBL",
        "UPI-THEAROGYA CAFE-VYAPAR.171813558689@",
        "UPI-MEENAKSHI S-MEENAKSHISANKAR2013@OKSBI",
        "OPENAI*CHATGP TSUBSCR",
        "MAGICPIN-CF.MAGICPIN@ICICI"
    ]
    
    for test in test_cases:
        category, confidence = categorizer.predict(test)
        print(f"{test[:30]:30} -> {category:15} ({confidence:.3f})")