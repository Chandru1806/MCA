# modules/ingestion/extract.py
import re
import pandas as pd
import pdfplumber
from datetime import datetime


# ---------------- Common primitives ----------------
DATE_RE = re.compile(r"^\d{2}[-/]\d{2}[-/]\d{2,4}\b")   # 01-07-2025 / 02/02/25
NUM = r"[+-]?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
NUM_RE = re.compile(f"^{NUM}$")

# Headers/footers/watermarks to ignore
NOISE_PATTERNS = [
    r"^Withdrawal\(Dr\)\s*$",
    r"^Deposit\(Cr\)\s*$",
    r"^Date\s+Narration.*Balance\s*$",
    r"^Date\s+Narration\s+Chq\./Ref\.No\..*Balance",
    r"^Page\s+\d+\s+of\s+\d+\s*$",
    r"^Statement Summary",
    r"^Statement of account",
    r"^Opening Balance",
    r"^Closing Balance",
    r"^Total Withdrawal Amount",
    r"^Total Deposit Amount",
    r"^Withdrawal Count",
    r"^Deposit Count",
    r"^End of Statement",
    r"This is system generated report",
    r"^From\s*:\s*\d{2}/\d{2}/\d{4}.*$",
    r"^\s*Account\s+Branch\b.*$",
    r"^\s*JOINTHOLDERS:.*$",
    r"HDFCBANKLIMITED",
    r"Closingbalanceincludesfunds"
]

def _is_noise(line: str) -> bool:
    s = (line or "").strip()
    if not s:
        return True
    for pat in NOISE_PATTERNS:
        if re.search(pat, s, flags=re.I):
            return True
    return False

def _lines(pdf_path: str):
    out = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            for ln in txt.splitlines():
                ln = ln.strip()
                if ln:
                    out.append(ln)
    return out

# ===================== Footer cleaner ====================
def clean_description(desc: str) -> str:
    """Truncate noisy footers from description."""
    if not isinstance(desc, str):
        return desc
    patterns = [
        "Contentsofthisstatement",
        "RegisteredOfficeAddress",
        "GSTIN",
        "Stateaccountbranch",
        "Thisstatement"
    ]
    for p in patterns:
        if p in desc:
            return desc.split(p)[0].strip()
    return desc.strip()

# ===================== HDFC Parser ========================
HDFC_HEADER_RE = re.compile(
    r"^Date\s+Narration\s+Chq\./Ref\.No\.\s+ValueDt\s+WithdrawalAmt\.\s+DepositAmt\.\s+ClosingBalance\s*$",
    re.I,
)

DEBIT_HINTS  = ["NWD", "ATM", "POS", "CARD", "DEBIT", "FASTAG", "BILL", "RECHARGE", "ZOMATO", "SWIGGY", "AMAZON", "FLIPKART", "IRCTC", "PCD", "CHRG"]
CREDIT_HINTS = ["NEFT", "IMPS", "CREDIT", "SALARY", "REV", "REFUND", "INTEREST", "REWARD", "REVERSAL", "UPI-REV", "REV-UPI"]

INLINE_VALUEDT_BLOCK = re.compile(
    r"(?:\bValueDt\b\s*)?\b\d{2}/\d{2}/\d{2,4}\b(?:\s+" + NUM + r"){1,2}",
    re.I,
)

def _looks_like_debit(narr: str) -> bool:
    u = (narr or "").upper()
    return any(k in u for k in DEBIT_HINTS)

def _looks_like_credit(narr: str) -> bool:
    u = (narr or "").upper()
    return any(k in u for k in CREDIT_HINTS)

def _clean_hdfc_narr(narr: str) -> str:
    s = narr
    s = INLINE_VALUEDT_BLOCK.sub("", s)
    s = re.sub(r"\s{2,}", " ", s).strip(" -:·•|*")
    return s.strip()

def parse_hdfc_df(pdf_path: str) -> pd.DataFrame:
    L_all = _lines(pdf_path)
    start = 0
    for i, ln in enumerate(L_all):
        if HDFC_HEADER_RE.search(ln):
            start = i + 1
            break
    L = [ln for ln in L_all[start:] if not _is_noise(ln)]
    recs, cur = [], None

    def finalize(date: str, narr_parts: list[str]):
        s = (date + " " + " ".join(narr_parts)).strip()
        parts = s.split()
        if not parts:
            return None
        date = parts[0]
        tail = parts[1:]

        nums = []
        for tok in reversed(tail):
            if NUM_RE.match(tok):
                nums.append(tok)
                if len(nums) == 3:
                    break
            elif nums:
                break
        nums = list(reversed(nums))

        narr = " ".join(tail)
        for tok in reversed(nums):
            if narr.endswith(tok):
                narr = narr[: -len(tok)].rstrip()

        narr = clean_description(_clean_hdfc_narr(narr))

        debit = credit = balance = ""
        if len(nums) == 3:
            debit, credit, balance = nums
        elif len(nums) == 2:
            balance = nums[-1]
            amt = nums[0]
            if _looks_like_credit(narr) and not _looks_like_debit(narr):
                credit = amt
            elif _looks_like_debit(narr) and not _looks_like_credit(narr):
                debit = amt
            else:
                debit = amt
        elif len(nums) == 1:
            balance = nums[0]

        chq_ref = ""
        mref = re.search(r"(?:UPI-\w+|[A-Za-z]{2,}\d{6,}|[A-Z]{2,}\d{4,}|[0-9]{6,})$", narr)
        if mref:
            chq_ref = mref.group(0).strip()
            narr = narr[: narr.rfind(chq_ref)].rstrip()

        return [date, narr, chq_ref, debit, credit, balance]

    for raw in L:
        if DATE_RE.match(raw):
            if cur:
                row = finalize(cur["date"], cur["narr"])
                if row:
                    recs.append(row)
            parts = raw.split(maxsplit=1)
            cur = {"date": parts[0], "narr": [parts[1]] if len(parts) > 1 else []}
        else:
            if cur:
                cur["narr"].append(raw)

    if cur:
        row = finalize(cur["date"], cur["narr"])
        if row:
            recs.append(row)

    return pd.DataFrame(recs, columns=["Date", "Narration", "Chq/Ref No", "Debit", "Credit", "Balance"])

# KOTAK + GENERIC parsers remain unchanged unless you want footer removal there as well.

# (If needed, you can apply `clean_description()` inside `parse_generic_df()` too)
# ======================================================================
# KOTAK
# ======================================================================

# Perfect tail core: "<amt>(Dr|Cr) <bal>(Dr|Cr)"
KOTAK_TAIL_CORE = re.compile(
    r"(?P<amount>\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\s*\((?P<ad>Dr|Cr)\)\s+"
    r"(?P<balance>\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\s*\((?P<bd>Dr|Cr)\)"
)

# Stuff that sometimes appears AFTER a valid tail (we strip it)
POST_TAIL_GARBAGE = re.compile(
    r"(?:"
    r"\s+for\s+pin"
    r"|"
    r"\s+[A-Z]{3,}\d{6,}(?:/\d{2}[:.]\d{2})?"       # BRKAN020725/17:26
    r"|"
    r"\s+/(?:[A-Za-z0-9-]{3,}(?:\s+[A-Za-z0-9-]{2,})*)\b"  # /JIO20PT..., /REFUND TO BEN, /KreditPe
    r"|"
    r"\s+FASTAG\b"
    r")+\s*$",
    re.I
)

def _strip_post_tail_garbage(s: str) -> str:
    if KOTAK_TAIL_CORE.search(s):
        s = POST_TAIL_GARBAGE.sub("", s)
    return s.strip()

def _try_match_kotak_tail(s: str):
    """Return (amount(ad), balance(bd)) or None."""
    s2 = _strip_post_tail_garbage(s)
    m = KOTAK_TAIL_CORE.search(s2)
    if not m:
        return None
    amt = f"{m.group('amount')}({m.group('ad')})"
    bal = f"{m.group('balance')}({m.group('bd')})"
    return amt, bal

def parse_kotak_df(pdf_path: str) -> pd.DataFrame:
    """
    Strategy:
      - Accumulate lines from a date until we find a Kotak tail on the joined text.
      - If tail found, strip tail+garbage and emit.
      - On new date without tail, emit incomplete (validator may reject).
      - Also attempt a tighter join of the last two lines (common wrap quirk).
    """
    L = [ln for ln in _lines(pdf_path) if not _is_noise(ln)]
    recs, cur = [], None

    def flush(force=False):
        nonlocal cur
        if not cur:
            return
        joined = " ".join(cur["narr"]).strip()

        # 1) direct try
        mb = _try_match_kotak_tail(joined)
        if mb:
            amt_s, bal_s = mb
            narr = KOTAK_TAIL_CORE.sub("", _strip_post_tail_garbage(joined)).strip()
            recs.append([cur["date"], narr, amt_s, bal_s])
            cur = None
            return

        # 2) tight merge last 2 lines
        if len(cur["narr"]) >= 2:
            tight = " ".join(cur["narr"][:-2] + [cur["narr"][-2] + " " + cur["narr"][-1]])
            mb2 = _try_match_kotak_tail(tight)
            if mb2:
                amt_s, bal_s = mb2
                narr = KOTAK_TAIL_CORE.sub("", _strip_post_tail_garbage(tight)).strip()
                recs.append([cur["date"], narr, amt_s, bal_s])
                cur = None
                return

        # 3) if still no tail
        if force:
            recs.append([cur["date"], joined, "", ""])
            cur = None

    for raw in L:
        if DATE_RE.match(raw):
            flush(force=True)
            parts = raw.split(maxsplit=1)
            date = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
            cur = {"date": date, "narr": [rest] if rest else []}
        else:
            if cur:
                cur["narr"].append(raw)
                if _try_match_kotak_tail(" ".join(cur["narr"]).strip()):
                    flush(force=False)

    flush(force=True)
    return pd.DataFrame(recs, columns=["Date", "Narration", "Amount (Dr/Cr)", "Balance (Dr/Cr)"])


# ======================================================================
# SBI
# ======================================================================

SBI_HEADER_RE = re.compile(
    r"^Txn\s+Date\s+Value\s+Date\s+Description\s+Ref\s*No\./Cheque\s*No\.\s+Debit\s+Credit\s+Balance\s*$",
    re.I,
)

SBI_FOOTER_PATTERNS = [
    r"The count of transactions for the selected date range exceeds 299",
    r"Please do not share your ATM",
    r"Bank never asks for such information",
    r"This is a computer generated statement",
    r"PIN \(Personal Identification Number\)",
    r"OTP \(One Time Password\)",
    r"does not require a signature",
]

def _is_sbi_footer(line: str) -> bool:
    """Check if a line is SBI footer/disclaimer."""
    for pat in SBI_FOOTER_PATTERNS:
        if re.search(pat, line, flags=re.I):
            return True
    return False


def parse_sbi_df(pdf_path: str) -> pd.DataFrame:
    """
    Extract transactions from SBI PDF statements.
    Works for tables with columns:
      Txn Date | Value Date | Description | Ref No./Cheque No. | Debit | Credit | Balance
    """
    import pdfplumber
    import pandas as pd
    import re

    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            try:
                tables = page.extract_tables()
                for t in tables:
                    if not t:
                        continue
                    # Find header row
                    header_row = None
                    for i, row in enumerate(t):
                        joined = " ".join(str(c or "") for c in row)
                        if re.search(r"Txn\s*Date", joined, flags=re.I) and re.search(r"Balance", joined, flags=re.I):
                            header_row = i
                            break
                    if header_row is not None:
                        header = [c.strip() if c else "" for c in t[header_row]]
                        data_rows = t[header_row + 1:]
                        df = pd.DataFrame(data_rows, columns=header)
                        all_tables.append(df)
            except Exception:
                continue

    if not all_tables:
        print("[WARN] No table detected in SBI statement.")
        return pd.DataFrame()

    df_raw = pd.concat(all_tables, ignore_index=True)

    # --- Relaxed mapping ---
    col_map = {}
    for c in df_raw.columns:
        cname = c.strip().lower().replace(".", "").replace("/", "")
        if "txn" in cname and "date" in cname:
            col_map[c] = "Date"
        elif "desc" in cname:
            col_map[c] = "Narration"
        elif "ref" in cname or "cheque" in cname:
            col_map[c] = "Ref_No"
        elif "debit" in cname:
            col_map[c] = "Debit"
        elif "credit" in cname:
            col_map[c] = "Credit"
        elif "balance" in cname:
            col_map[c] = "Balance"

    df_raw.rename(columns=col_map, inplace=True)

    # --- Ensure all expected columns exist ---
    for col in ["Date", "Narration", "Ref_No", "Debit", "Credit", "Balance"]:
        if col not in df_raw.columns:
            df_raw[col] = ""

    # --- Clean data ---
    for col in ["Date", "Narration", "Debit", "Credit", "Balance"]:
        df_raw[col] = (
            df_raw[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    # --- Drop totals and blank rows ---
    df_raw = df_raw[~df_raw["Date"].str.contains("Total|Closing|Opening", case=False, na=False)]
    df_raw = df_raw[df_raw["Date"].str.strip() != ""]

    return df_raw[["Date", "Narration", "Ref_No", "Debit", "Credit", "Balance"]]
import pdfplumber
import pandas as pd
import re

def parse_icici_df(pdf_path: str) -> pd.DataFrame:
    """
    Robust ICICI Bank PDF parser that handles multi-line grid-based tables.
    Extracts Value Date, Transaction Date, Remarks, Debit, Credit, Balance.
    """
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                for r in table:
                    row = [str(x).strip().replace("\n", " ") if x else "" for x in r]
                    # Skip header or empty lines
                    joined = " ".join(row).lower()
                    if "transaction remarks" in joined or "value date" in joined or "balance" in joined:
                        continue
                    if not any(row):
                        continue

                    rows.append(row)

    # Convert to DataFrame and infer layout
    df = pd.DataFrame(rows)

    # Try to auto-detect ICICI table structure
    if df.shape[1] >= 8:
        df = df.iloc[:, :8]  # first 8 columns
        df.columns = [
            "S.No", "Value Date", "Transaction Date", "Cheque Number",
            "Transaction Remarks", "Withdrawal Amount (INR)",
            "Deposit Amount (INR)", "Balance (INR)"
        ]
    else:
        # fallback for merged-column PDFs
        df.columns = ["col" + str(i) for i in range(len(df.columns))]

    # Filter valid transaction rows only (contains dates)
    df = df[df["Transaction Date"].str.match(r"\d{2}/\d{2}/\d{4}", na=False)]

    # Build standardized DataFrame
    df_std = pd.DataFrame({
        "Date": df["Transaction Date"].fillna(df["Value Date"]),
        "Narration": df["Transaction Remarks"],
        "Debit": df["Withdrawal Amount (INR)"].replace(",", "", regex=True),
        "Credit": df["Deposit Amount (INR)"].replace(",", "", regex=True),
        "Balance": df["Balance (INR)"].replace(",", "", regex=True)
    })

    # Drop invalid or blank rows
    df_std = df_std[df_std["Date"].notna() & df_std["Narration"].notna()]
    df_std = df_std[df_std["Date"].str.contains(r"\d{2}/\d{2}/\d{4}")]

    print(f"[ICICI] ✅ Extracted {len(df_std)} valid transactions.")
    return df_std