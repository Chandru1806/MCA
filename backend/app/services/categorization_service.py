from app.services.Categorization_Model import OptimizedFinalClassifier
from app.models.transaction import Transaction
from app.models.transaction_category import TransactionCategory
from app import db

class CategorizationService:
    
    def __init__(self):
        self.classifier = OptimizedFinalClassifier()
    
    def categorize_transactions(self, statement_id: int):
        """Categorize all transactions for a statement"""
        transactions = Transaction.query.filter_by(statement_id=statement_id).all()
        
        if not transactions:
            raise ValueError("No transactions found for this statement")
        
        # Check if already categorized
        existing_count = TransactionCategory.query.join(
            Transaction, TransactionCategory.transaction_id == Transaction.transaction_id
        ).filter(Transaction.statement_id == statement_id).count()
        
        if existing_count > 0:
            raise ValueError(f"Transactions already categorized for this statement ({existing_count} records)")
        
        categories = []
        for txn in transactions:
            # Get predictions
            final_cat, final_conf = self.classifier.predict(txn.description)
            rule_cat, rule_conf = self.classifier._rule_classify(txn.description)
            semantic_cat, semantic_conf = self.classifier._semantic_classify(txn.description)
            
            # Extract merchant and update transaction
            merchant = self.classifier._extract_merchant(txn.description)
            txn.merchant_name = merchant
            
            # Determine method
            method = 'RULE_BASED' if rule_conf >= 0.90 else 'HYBRID'
            
            # Create category record
            category = TransactionCategory(
                profile_id=txn.profile_id,
                transaction_id=txn.transaction_id,
                category_name=final_cat,
                confidence_score=round(float(final_conf), 2),
                classification_method=method,
                rule_based_prediction=rule_cat,
                ml_prediction=semantic_cat
            )
            categories.append(category)
        
        db.session.bulk_save_objects(categories)
        db.session.commit()
        
        return len(categories)
