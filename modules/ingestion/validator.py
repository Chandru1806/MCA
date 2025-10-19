import re
import pandas as pd
from datetime import datetime

# -------- Numbers --------
_NUM_BODY = r"[+-]?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
NUM_RE = re.compile(rf"^{_NUM_BODY}$")

def _to_float_or_none(x):
    if x is None:
        return None
    s = str(x).strip().replace(",", "")
    if s in ("", "+", "-"):
        return None
    try:
        return float(s)
    except Exception:
        return None

def _fmt2(x) -> str:
    try:
        return f"{float(x):.2f}"
    except Exception:
        return ""

def _norm_num_2d(x: str) -> str:
    v = _to_float_or_none(x)
    return _fmt2(v) if v is not None else ""

# -------- Dates --------
_DATE_FORMATS = (
    "%d-%m-%Y", "%d-%m-%y",
    "%d/%m/%Y", "%d/%m/%y",
    "%d-%b-%Y", "%d-%b-%y",
    "%d-%B-%Y", "%d-%B-%y",
)

def _parse_date_iso(d: str) -> str:
    if d is None:
        return ""
    s = str(d).strip()
    if not s:
        return ""
    s_try = s.replace("/", "-")
    for cand in (s_try, s_try.title()):
        for fmt in _DATE_FORMATS:
            try:
                dt = datetime.strptime(cand, fmt)
                return dt.strftime("%Y-%m-%d")
            except Exception:
                pass
    return ""

# -------- Kotak helpers --------
_DR_CR_TAG = re.compile(r"\((Dr|Cr)\)", re.I)

def _split_kotak_amount(amt_drcr: str) -> tuple[str, str]:
    if not amt_drcr:
        return "", ""
    s = str(amt_drcr).strip()
    tag = None
    m = _DR_CR_TAG.search(s)
    if m:
        tag = m.group(1).lower()
        s = _DR_CR_TAG.sub("", s).strip()
    val = _norm_num_2d(s)
    if val == "":
        return "", ""
    if tag == "dr":
        return val, ""
    if tag == "cr":
        return "", val
    return val, ""  # default debit

def _strip_kotak_balance_tag(bal_drcr: str) -> str:
    if not bal_drcr:
        return ""
    s = _DR_CR_TAG.sub("", str(bal_drcr)).strip()
    return _norm_num_2d(s)

# -------- Splitters --------
def split_std_rejects_kotak(df_raw: pd.DataFrame, bank_name: str = "KOTAK"):
    std_rows, rej_rows = [], []
    bank = (bank_name or "KOTAK").upper()
    if df_raw is None or df_raw.empty:
        return pd.DataFrame(std_rows), pd.DataFrame(rej_rows)

    for _, r in df_raw.iterrows():
        raw_date = str(r.get("Date", "")).strip()
        narr = str(r.get("Narration", "")).strip()
        amt = str(r.get("Amount (Dr/Cr)", "")).strip()
        bal = str(r.get("Balance (Dr/Cr)", "")).strip()

        iso = _parse_date_iso(raw_date)
        debit, credit = _split_kotak_amount(amt)
        bal_clean = _strip_kotak_balance_tag(bal)

        reasons = []
        if iso == "":
            reasons.append("bad_date")
        if bal_clean == "":
            reasons.append("bad_balance")

        if reasons:
            rej_rows.append({
                "Bank_Name": bank,
                "Raw_Date": raw_date,
                "Raw_Narration": narr,
                "Raw_Amount": amt,
                "Raw_Balance": bal,
                "Reason": ";".join(reasons),
                "Suggest_Date": iso,
                "Suggest_Debit": debit,
                "Suggest_Credit": credit,
                "Suggest_Balance": bal_clean
            })
            continue

        if debit == "" and credit == "":
            debit, credit = "0.00", "0.00"

        std_rows.append({
            "Transaction_Date": iso,
            "Description": narr,
            "Debit_Amount": debit,
            "Credit_Amount": credit,
            "Balance": bal_clean,
            "Bank_Name": bank,
        })

    return pd.DataFrame(std_rows), pd.DataFrame(rej_rows)

def split_std_rejects_hdfc_like(df_raw: pd.DataFrame, bank_name: str = "HDFC"):
    std_rows, rej_rows = [], []
    bank = (bank_name or "HDFC").upper()
    if df_raw is None or df_raw.empty:
        return pd.DataFrame(std_rows), pd.DataFrame(rej_rows)

    for _, r in df_raw.iterrows():
        raw_date = str(r.get("Date", "")).strip()
        narr = " ".join([
            str(r.get("Narration", "")).strip(),
            str(r.get("Chq/Ref No", "")).strip()
        ]).strip()

        raw_debit = str(r.get("Debit", "") or "").strip()
        raw_credit = str(r.get("Credit", "") or "").strip()
        raw_balance = str(r.get("Balance", "") or "").strip()

        iso = _parse_date_iso(raw_date)
        debit_n = _norm_num_2d(raw_debit)
        credit_n = _norm_num_2d(raw_credit)
        bal_n = _norm_num_2d(raw_balance)

        reasons = []
        if iso == "":
            reasons.append("bad_date")
        if bal_n == "":
            reasons.append("bad_balance")

        # NEW: if both debit and credit are > 0 → reject as ambiguous
        if debit_n not in ("", "0.00") and credit_n not in ("", "0.00"):
            reasons.append("both_amounts_present")

        if reasons:
            rej_rows.append({
                "Bank_Name": bank,
                "Raw_Date": raw_date,
                "Raw_Narration": narr,
                "Raw_Debit": raw_debit,
                "Raw_Credit": raw_credit,
                "Raw_Balance": raw_balance,
                "Reason": ";".join(reasons),
                "Suggest_Date": iso,
                "Suggest_Debit": debit_n,
                "Suggest_Credit": credit_n,
                "Suggest_Balance": bal_n
            })
            continue

        if debit_n == "" and credit_n == "":
            debit_n, credit_n = "0.00", "0.00"

        std_rows.append({
            "Transaction_Date": iso,
            "Description": narr,
            "Debit_Amount": debit_n,
            "Credit_Amount": credit_n,
            "Balance": bal_n,
            "Bank_Name": bank,
        })

    return pd.DataFrame(std_rows), pd.DataFrame(rej_rows)
