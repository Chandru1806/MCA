import pandas as pd
from datetime import datetime
from app.models.transaction import Transaction
from app.models.bank_statement import BankStatement
from app import db
import os

class TransactionService:
    
    @staticmethod
    def import_from_csv(statement_id: int):
        """Import transactions from CSV into database"""
        statement = BankStatement.query.get(statement_id)
        if not statement:
            raise ValueError("Statement not found")
        
        csv_path = statement.normalized_csv_path or statement.extracted_csv_path
        if not csv_path:
            raise ValueError("No CSV file found")
        
        if not os.path.exists(csv_path):
            raise ValueError(f"CSV file not found at path: {csv_path}")
        
        df = pd.read_csv(csv_path)
        
        # Check if transactions already imported
        existing_count = Transaction.query.filter_by(statement_id=statement_id).count()
        if existing_count > 0:
            raise ValueError(f"Transactions already imported for this statement ({existing_count} records)")
        
        transactions = []
        for _, row in df.iterrows():
            transaction = Transaction(
                profile_id=statement.profile_id,
                statement_id=statement_id,
                transaction_date=pd.to_datetime(row['Transaction_Date']).date(),
                description=str(row['Description']),
                debit_amount=row.get('Debit_Amount') if pd.notna(row.get('Debit_Amount')) else None,
                credit_amount=row.get('Credit_Amount') if pd.notna(row.get('Credit_Amount')) else None,
                balance=row.get('Balance') if pd.notna(row.get('Balance')) else None,
                is_repaired=bool(row.get('is_repaired', False))
            )
            transactions.append(transaction)
        
        db.session.bulk_save_objects(transactions)
        db.session.commit()
        
        return len(transactions)
