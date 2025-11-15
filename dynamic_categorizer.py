import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import pickle
import os

class DynamicTransactionCategorizer:
    def __init__(self):
        self.rule_patterns = self._build_rule_patterns()
        self.ml_model = None
        self.categories = [
            'Food', 'Travel', 'Bills', 'Shopping', 'Entertainment', 
            'Salary', 'Investments', 'EMI', 'Health', 'Education',
            'Person', 'Bank_Charges', 'Recharge', 'Groceries', 'Others'
        ]
        
    def _build_rule_patterns(self):
        """High-confidence keyword patterns for rule-based classification"""
        return {
            'Food': [
                'zomato', 'swiggy', 'dominos', 'pizza', 'mcdonald', 'kfc', 'burger',
                'restaurant', 'cafe', 'food', 'biryani', 'hotel', 'canteen'
            ],
            'Travel': [
                'redbus', 'irctc', 'uber', 'ola', 'makemytrip', 'goibibo', 'indigo',
                'spicejet', 'railway', 'flight', 'bus', 'taxi', 'metro'
            ],
            'Bills': [
                'electricity', 'tneb', 'bescom', 'water', 'bwssb', 'gas', 'broadband',
                'wifi', 'internet', 'dth', 'tatasky', 'airtel', 'jio', 'vi'
            ],
            'Shopping': [
                'amazon', 'flipkart', 'myntra', 'ajio', 'nykaa', 'snapdeal',
                'shopping', 'mall', 'store', 'retail', 'westside', 'reliance'
            ],
            'Entertainment': [
                'netflix', 'hotstar', 'prime', 'bookmyshow', 'movie', 'cinema',
                'youtube', 'spotify', 'gaming', 'subscription'
            ],
            'Salary': [
                'salary', 'payroll', 'tcs', 'infosys', 'wipro', 'employee',
                'credited by', 'monthly salary'
            ],
            'Investments': [
                'mutual fund', 'sip', 'fd', 'nps', 'stock', 'dividend',
                'investment', 'zerodha', 'groww', 'upstox'
            ],
            'EMI': [
                'emi', 'loan', 'installment', 'bajaj', 'hdfc emi', 'kotak emi',
                'repayment', 'credit card emi'
            ],
            'Health': [
                'apollo', 'hospital', 'pharmacy', 'medplus', 'doctor',
                'medical', 'clinic', 'health', 'medicine'
            ],
            'Education': [
                'school', 'college', 'university', 'fees', 'tuition', 'byjus',
                'vedantu', 'coursera', 'udemy', 'education'
            ],
            'Bank_Charges': [
                'atm charge', 'sms fee', 'debit card fee', 'account maintenance',
                'neft charge', 'bank charge'
            ],
            'Recharge': [
                'recharge', 'mobile recharge', 'data pack', 'prepaid', 'postpaid'
            ],
            'Groceries': [
                'bigbasket', 'grofers', 'dmart', 'grocery', 'vegetables',
                'instamart', 'blinkit', 'zepto', 'dunzo'
            ]
        }
    
    def _preprocess_description(self, description):
        """Clean and normalize transaction description"""
        if pd.isna(description):
            return ""
        
        text = str(description).lower()
        # Remove transaction IDs and reference numbers
        text = re.sub(r'\b\d{10,}\b', '', text)
        # Remove UPI handles but keep merchant names
        text = re.sub(r'@[a-z0-9]+', '', text)
        # Remove special characters except spaces and hyphens
        text = re.sub(r'[^\w\s-]', ' ', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _rule_based_classify(self, description):
        """Apply rule-based classification using keyword matching"""
        clean_desc = self._preprocess_description(description)
        
        for category, keywords in self.rule_patterns.items():
            for keyword in keywords:
                if keyword in clean_desc:
                    return category, 1.0  # High confidence for rule-based
        
        return None, 0.0
    
    def _prepare_training_data(self):
        """Generate comprehensive training data for ML model"""
        training_data = []
        
        # Food examples
        food_examples = [
            "upi zomato order payment", "swiggy food delivery", "dominos pizza online",
            "mcdonald burger king", "kfc chicken bucket", "restaurant bill payment",
            "hotel dining charges", "cafe coffee day", "biryani house order"
        ]
        
        # Travel examples  
        travel_examples = [
            "redbus ticket booking", "irctc train reservation", "uber cab ride",
            "ola auto payment", "makemytrip flight", "indigo airline ticket",
            "metro card recharge", "bus ticket online"
        ]
        
        # Bills examples
        bills_examples = [
            "electricity bill tneb", "water bill bwssb", "gas cylinder booking",
            "broadband bill airtel", "dth recharge tatasky", "internet bill payment"
        ]
        
        # Shopping examples
        shopping_examples = [
            "amazon purchase order", "flipkart electronics", "myntra clothing",
            "westside fashion store", "reliance digital", "shopping mall payment"
        ]
        
        # Add all categories with examples
        categories_data = {
            'Food': food_examples,
            'Travel': travel_examples, 
            'Bills': bills_examples,
            'Shopping': shopping_examples,
            'Entertainment': ["netflix subscription", "bookmyshow ticket", "youtube premium"],
            'Salary': ["monthly salary credit", "payroll payment", "employee salary"],
            'Investments': ["mutual fund sip", "stock purchase", "fd investment"],
            'EMI': ["loan emi payment", "credit card emi", "home loan installment"],
            'Health': ["hospital bill payment", "pharmacy medicine", "doctor consultation"],
            'Education': ["school fees payment", "college tuition", "online course fee"],
            'Bank_Charges': ["atm withdrawal charge", "account maintenance fee"],
            'Recharge': ["mobile recharge", "data pack purchase"],
            'Groceries': ["grocery shopping", "vegetable purchase", "supermarket bill"],
            'Person': ["transfer to friend", "family payment", "personal transfer"],
            'Others': ["cash deposit", "unknown transaction", "miscellaneous payment"]
        }
        
        for category, examples in categories_data.items():
            for example in examples:
                training_data.append((example, category))
        
        return training_data
    
    def train_ml_model(self):
        """Train ML model on synthetic and real data"""
        training_data = self._prepare_training_data()
        
        X = [self._preprocess_description(desc) for desc, _ in training_data]
        y = [cat for _, cat in training_data]
        
        self.ml_model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=1000)),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        self.ml_model.fit(X, y)
        
    def predict_category(self, description, amount=None, transaction_type=None):
        """Hybrid prediction: Rule-based → ML fallback"""
        
        # Step 1: Try rule-based classification
        rule_category, rule_confidence = self._rule_based_classify(description)
        if rule_category:
            return rule_category, rule_confidence
        
        # Step 2: Use ML model for unknown patterns
        if self.ml_model is None:
            self.train_ml_model()
        
        clean_desc = self._preprocess_description(description)
        if not clean_desc:
            return 'Others', 0.1
        
        try:
            ml_prediction = self.ml_model.predict([clean_desc])[0]
            ml_proba = self.ml_model.predict_proba([clean_desc]).max()
            
            # Apply business logic based on amount and type
            if amount and transaction_type:
                ml_prediction = self._apply_business_rules(
                    ml_prediction, description, amount, transaction_type
                )
            
            return ml_prediction, ml_proba
            
        except Exception:
            return 'Others', 0.1
    
    def _apply_business_rules(self, prediction, description, amount, transaction_type):
        """Apply business logic to refine predictions"""
        
        # Large amounts likely to be EMI/Salary/Investments
        if amount > 10000:
            if transaction_type == 'credit':
                return 'Salary' if 'salary' in description.lower() else prediction
            elif 'emi' in description.lower() or 'loan' in description.lower():
                return 'EMI'
        
        # Small amounts likely to be recharge/transport
        if amount < 100:
            if any(word in description.lower() for word in ['recharge', 'mobile', 'data']):
                return 'Recharge'
            elif any(word in description.lower() for word in ['metro', 'bus', 'auto']):
                return 'Travel'
        
        return prediction
    
    def categorize_transactions(self, df):
        """Categorize all transactions in dataframe"""
        results = []
        
        for _, row in df.iterrows():
            description = row.get('Description', '')
            debit_amt = row.get('Debit_Amount', 0)
            credit_amt = row.get('Credit_Amount', 0)
            
            amount = debit_amt if debit_amt > 0 else credit_amt
            transaction_type = 'debit' if debit_amt > 0 else 'credit'
            
            category, confidence = self.predict_category(description, amount, transaction_type)
            
            results.append({
                'Transaction_ID': row.get('Transaction_ID', ''),
                'Transaction_Date': row.get('Transaction_Date', ''),
                'Description': description,
                'Debit_Amount': debit_amt,
                'Credit_Amount': credit_amt,
                'Balance': row.get('Balance', 0),
                'Bank_Name': row.get('Bank_Name', ''),
                'Category': category,
                'Confidence': round(confidence, 3)
            })
        
        return pd.DataFrame(results)
    
    def save_model(self, filepath):
        """Save trained model to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.ml_model, f)
    
    def load_model(self, filepath):
        """Load trained model from file"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.ml_model = pickle.load(f)

# Usage Example
if __name__ == "__main__":
    # Initialize categorizer
    categorizer = DynamicTransactionCategorizer()
    
    # Load transaction data
    df = pd.read_csv("transactions_dataset.csv")
    
    # Categorize transactions
    categorized_df = categorizer.categorize_transactions(df)
    
    # Save results
    categorized_df.to_csv("categorized_transactions_final.csv", index=False)
    
    # Save model for future use
    categorizer.save_model("transaction_categorizer_model.pkl")
    
    print(f"✅ Categorized {len(categorized_df)} transactions")
    print(f"📊 Category distribution:")
    print(categorized_df['Category'].value_counts())