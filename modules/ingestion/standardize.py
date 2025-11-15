import os
import re
import uuid
import pandas as pd
from .validator import split_std_rejects_kotak, split_std_rejects_hdfc_like, split_std_rejects_sbi, split_std_rejects_icici

# ---------------- Common Schema ----------------
COMMON_COLS = [
    "Transaction_ID",
    "Transaction_Date",
    "Description",
    "Debit_Amount",
    "Credit_Amount",
    "Balance",
    "Bank_Name",
]

NUM = r"[+-]?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
_VALUE_DT_TAIL = re.compile(
    rf"\s+\d{{2}}/\d{{2}}/\d{{2,4}}(?:\s+{NUM}){{1,2}}\s*$",
    re.I
)
_TRAILING_NUM = re.compile(rf"\s+{NUM}\s*$", re.I)
_TRAILING_DATE_ONLY = re.compile(r"\s+\d{2}[-/]\d{2}[-/]\d{2,4}\s*$")
_SYS_TAIL = re.compile(
    r"(?:"  # remove trailing system info fragments
    r"\s+for\s+pin"
    r"|"
    r"\s+[A-Z]{3,}\d{6,}(?:/\d{2}[:.]\d{2})?"
    r"|"
    r"\s+/(?:[A-Za-z0-9-]{3,}(?:\s+[A-Za-z0-9-]{2,})*)\b"
    r")+"
    r"\s*$",
    re.I
)
_HDFC_ADDR = re.compile(r"HDFC\s*Bank\s*House.*?Mumbai\s*\d{6}", re.I)
_DATE_AMT_BAL_INLINE = re.compile(
    r"\b\d{2}/\d{2}/\d{2,4}\s+"
    r"[+-]?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})\s+"
    r"[+-]?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})\b"
)
_WS2 = re.compile(r"\s{2,}")


# =====================================================
# Clean Description
# =====================================================
def _clean_desc(text: str) -> str:
    if not isinstance(text, str):
        return text
    s = text
    s = _HDFC_ADDR.sub("", s)
    s = re.split(r"(HDFC\s*BANK.*|HDFCBANKLIMITED.*)", s, flags=re.I)[0]
    s = _DATE_AMT_BAL_INLINE.sub("", s)
    s = _VALUE_DT_TAIL.sub("", s)
    s = _TRAILING_DATE_ONLY.sub("", s)
    s = _SYS_TAIL.sub("", s)
    s = _TRAILING_NUM.sub("", s)
    s = s.strip(" -:·•|")
    s = _WS2.sub(" ", s).strip()
    return s


# =====================================================
# Numeric Format Helpers
# =====================================================
def _fmt2(x) -> str:
    try:
        if x is None or str(x).strip() == "":
            return ""
        return f"{float(str(x).replace(',', '').strip()):.2f}"
    except Exception:
        return ""


# =====================================================
# Enforce Schema + Data Types
# =====================================================
def _enforce_schema_and_types(std_df: pd.DataFrame, bank_upper: str) -> pd.DataFrame:
    if std_df is None or std_df.empty:
        return pd.DataFrame(columns=COMMON_COLS)

    df = std_df.copy()
    for c in ["Transaction_Date", "Description", "Debit_Amount", "Credit_Amount", "Balance", "Bank_Name"]:
        if c not in df.columns:
            df[c] = ""

    df["Description"]   = df["Description"].astype(str).apply(_clean_desc)
    df["Debit_Amount"]  = df["Debit_Amount"].apply(_fmt2)
    df["Credit_Amount"] = df["Credit_Amount"].apply(_fmt2)
    df["Balance"]       = df["Balance"].apply(_fmt2)
    df["Bank_Name"]     = (bank_upper or "UNKNOWN").upper()

    df.insert(0, "Transaction_ID", [uuid.uuid4().hex[:12] for _ in range(len(df))])
    for c in COMMON_COLS:
        if c not in df.columns:
            df[c] = ""
    return df[COMMON_COLS]


# =====================================================
# Log Summary
# =====================================================
def _log_quality(file_base: str, bank: str, std_df: pd.DataFrame, rej_df: pd.DataFrame):
    n_std = 0 if std_df is None else len(std_df)
    n_rej = 0 if rej_df is None else len(rej_df)
    total = n_std + n_rej
    rej_rate = (n_rej / total * 100.0) if total else 0.0
    print(f"[INGEST] {file_base} [{bank}] → STD: {n_std}, REJECTS: {n_rej}, Total: {total}, Reject rate: {rej_rate:.1f}%")


# =====================================================
# Main Standardization Entry Point
# =====================================================
def standardize_and_write(df_raw: pd.DataFrame, bank_name: str, base_name: str, out_dir: str):
    """
    Applies the appropriate validator for the bank, standardizes column types,
    and writes STD and REJECT CSVs to the output directory.
    """
    os.makedirs(out_dir, exist_ok=True)
    bank = (bank_name or "UNKNOWN").upper()

    # --- Select appropriate validator ---
    if bank == "KOTAK":
        std_df, rej_df = split_std_rejects_kotak(df_raw, bank)
    elif bank == "SBI":
        std_df, rej_df = split_std_rejects_sbi(df_raw, bank)
    elif bank == "ICICI":
        std_df, rej_df = split_std_rejects_icici(df_raw, bank)
    else:
        std_df, rej_df = split_std_rejects_hdfc_like(df_raw, bank)

    # --- Enforce schema ---
    std_df = _enforce_schema_and_types(std_df, bank)

    # --- Output file paths ---
    std_csv = os.path.join(out_dir, f"{base_name}__STD_{bank}.csv")
    rej_csv = os.path.join(out_dir, f"{base_name}__REJECTS_{bank}.csv")

    # --- Write CSVs ---
    std_df.to_csv(std_csv, index=False, encoding="utf-8-sig")
    (rej_df if rej_df is not None else pd.DataFrame()).to_csv(rej_csv, index=False, encoding="utf-8-sig")

    # --- Log summary ---
    _log_quality(base_name, bank, std_df, rej_df)
    return std_csv, rej_csv
