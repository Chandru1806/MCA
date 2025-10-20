# repair/repair_rejects.py

import os
import pandas as pd

def split_column_values(val):
    """Split string by linebreak if possible."""
    try:
        return val.split("\n") if isinstance(val, str) else []
    except Exception:
        return []

def repair_reject_file(input_path, bank_name, output_path=None):
    print(f"🔧 Reading reject file: {input_path}")
    
    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

    if df.empty or df.shape[0] == 0:
        print(f"❌ {os.path.basename(input_path)} is empty.")
        return None

    print(f"🔍 Attempting repair for: {os.path.basename(input_path)} | Bank: {bank_name}")

    # Expected multi-line format reject columns
    expected_columns = ["Transaction_Date", "Description", "Debit_Amount", "Credit_Amount", "Balance"]
    if not all(col in df.columns for col in expected_columns):
        print("❌ Missing expected multiline reject format. Reject file is not repairable.")
        print(f"Found columns: {list(df.columns)}")
        return None

    try:
        # Split each field (multiline) into lists
        date_col = split_column_values(df["Transaction_Date"].iloc[0])
        desc_col = split_column_values(df["Description"].iloc[0])
        debit_col = split_column_values(df["Debit_Amount"].iloc[0])
        credit_col = split_column_values(df["Credit_Amount"].iloc[0])
        balance_col = split_column_values(df["Balance"].iloc[0])

        max_len = max(len(date_col), len(desc_col), len(debit_col), len(credit_col), len(balance_col))

        def safe(lst, i):
            return lst[i].strip() if i < len(lst) else ""

        # Rebuild cleaned row-wise dataframe
        repaired_rows = []
        for i in range(max_len):
            repaired_rows.append({
                "Transaction_ID": f"{bank_name.upper()}_R_{i+1:05d}",
                "Transaction_Date": safe(date_col, i),
                "Description": safe(desc_col, i),
                "Debit_Amount": safe(debit_col, i),
                "Credit_Amount": safe(credit_col, i),
                "Balance": safe(balance_col, i),
                "Bank_Name": bank_name.upper()
            })

        repaired_df = pd.DataFrame(repaired_rows)

        # Output file
        output_file = output_path or input_path.replace("__REJECTS_", "__RECOVERED_")
        repaired_df.to_csv(output_file, index=False)
        print(f"✅ Repaired and saved: {output_file}")
        return repaired_df

    except Exception as e:
        print(f"❌ Exception during repair logic: {e}")
        return None
