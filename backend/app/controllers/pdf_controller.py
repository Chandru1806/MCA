import os
import uuid
import traceback
import pandas as pd
from werkzeug.utils import secure_filename
from app import db
from app.models.bank_statement import BankStatement
from app.services.ingestion.detect import detect_bank
from app.services.ingestion.extract import parse_hdfc_df, parse_kotak_df, parse_sbi_df, parse_icici_df
from app.services.ingestion.standardize import standardize_and_write

class PDFController:
    
    @staticmethod
    def process_pdf(pdf_file, profile_id, upload_dir, output_dir, bank):
        batch_id = str(uuid.uuid4())[:8]
        safe_name = secure_filename(pdf_file.filename)
        file_path = os.path.join(upload_dir, f"{batch_id}_{safe_name}")
        
        pdf_file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        # Create DB record - PENDING
        statement = BankStatement(
            profile_id=profile_id,
            bank_name=bank,
            file_name=pdf_file.filename,
            file_path=file_path,
            file_size_bytes=file_size,
            processing_status='PENDING'
        )
        db.session.add(statement)
        db.session.commit()
        
        try:
            # Update to PROCESSING
            statement.processing_status = 'PROCESSING'
            db.session.commit()
            
            # Extract transactions
            if bank == "HDFC":
                df_raw = parse_hdfc_df(file_path)
            elif bank == "KOTAK":
                df_raw = parse_kotak_df(file_path)
            elif bank == "SBI":
                df_raw = parse_sbi_df(file_path)
            elif bank == "ICICI":
                df_raw = parse_icici_df(file_path)
            else:
                df_raw = parse_hdfc_df(file_path)
            
            # Standardize
            base = os.path.splitext(os.path.basename(file_path))[0]
            std_csv, rej_csv = standardize_and_write(df_raw, bank, base, output_dir)
            
            # Count transactions
            transaction_count = 0
            if os.path.exists(std_csv):
                df = pd.read_csv(std_csv)
                transaction_count = len(df)
            
            # Update to COMPLETED
            statement.extracted_csv_path = std_csv
            statement.normalized_csv_path = std_csv
            statement.processing_status = 'COMPLETED'
            db.session.commit()
            
            return {
                'statement_id': str(statement.file_id),
                'bank_name': bank,
                'transaction_count': transaction_count,
                'csv_filename': os.path.basename(std_csv)
            }
            
        except Exception as e:
            # Update to FAILED
            statement.processing_status = 'FAILED'
            statement.error_message = str(e)
            db.session.commit()
            raise
