import pandas as pd
import argparse
import os


def safe_float(val):
    try:
        val = str(val).replace(",", "").strip()
        return float(val) if val else None
    except:
        return None


def repair_using_surrounding_balances(df):
    repaired = df.copy()
    repaired.reset_index(drop=True, inplace=True)

    for i in range(1, len(repaired) - 1):
        row = repaired.iloc[i]

        # Check if both debit, credit, and balance are 0 or missing
        debit = safe_float(row.get("Debit_Amount"))
        credit = safe_float(row.get("Credit_Amount"))
        balance = safe_float(row.get("Balance"))

        if (not debit and not credit and not balance):
            prev_bal = safe_float(repaired.iloc[i - 1].get("Balance"))
            next_bal = safe_float(repaired.iloc[i + 1].get("Balance"))

            if prev_bal is None or next_bal is None:
                continue  # Skip if surrounding balances are unavailable

            diff = round(prev_bal - next_bal, 2)

            # Get the next row’s known amount to refine logic
            next_debit = safe_float(repaired.iloc[i + 1].get("Debit_Amount"))
            next_credit = safe_float(repaired.iloc[i + 1].get("Credit_Amount"))

            if next_debit:
                inferred_debit = round(diff - next_debit, 2)
                repaired.at[i, "Debit_Amount"] = inferred_debit if inferred_debit > 0 else ""
                repaired.at[i, "Balance"] = round(prev_bal - inferred_debit, 2)
                repaired.at[i, "Credit_Amount"] = ""
            elif next_credit:
                inferred_credit = round(diff + next_credit, 2)
                repaired.at[i, "Credit_Amount"] = inferred_credit if inferred_credit > 0 else ""
                repaired.at[i, "Balance"] = round(prev_bal + inferred_credit, 2)
                repaired.at[i, "Debit_Amount"] = ""
            else:
                # Fallback: just store the diff in debit
                repaired.at[i, "Debit_Amount"] = diff if diff > 0 else ""
                repaired.at[i, "Balance"] = round(prev_bal - diff, 2)
                repaired.at[i, "Credit_Amount"] = ""

    return repaired


def run(input_csv):
    df = pd.read_csv(input_csv)

    # Ensure required columns exist
    for col in ["Debit_Amount", "Credit_Amount", "Balance"]:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    repaired_df = repair_using_surrounding_balances(df)
    base, ext = os.path.splitext(input_csv)
    output_csv = base + "__REPAIRED" + ext
    repaired_df.to_csv(output_csv, index=False)
    print(f"[✅] Repaired CSV saved to: {output_csv}")
    return output_csv


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input CSV file path")
    args = parser.parse_args()
    run(args.input)
