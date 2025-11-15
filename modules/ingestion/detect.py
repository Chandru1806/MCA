import re
import pdfplumber

BANK_PATTERNS = {
    "HDFC": [
        r"\bHDFC\s*BANK\b",
        r"\bHDFC\s*BANK\s*LTD\b",
        r"\bHDFCBANKLTD\b",
        r"\bHDFCBANK\b",
        r"Statement\s*of\s*account.*HDFC",
    ],
    "KOTAK": [
        r"\bKOTAK\s*MAHINDRA\s*BANK\b",
        r"\bKOTAK\b",
    ],
    "SBI": [
        r"\bSTATE\s*BANK\s*OF\s*INDIA\b",
        r"\bSBI\b",
        # ✅ Generalized — works with or without dates
        r"Account\s*Statement.*State\s*Bank\s*of\s*India",
        r"Account\s*Statement.*SBI",
    ],
   "ICICI": [
        r"\bICICI\s*BANK\b",
        r"Account\s*Statement.*ICICI",
        r"ICICIBANK",
    ],
}

def detect_bank(pdf_path: str) -> str:
    """
    Detects the issuing bank from the first 2 pages of a PDF statement.
    Returns: 'HDFC', 'KOTAK', 'SBI', or 'UNKNOWN'
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for pg in pdf.pages[:2]:  # First two pages usually enough
                page_text = (pg.extract_text() or "").strip()
                text += "\n" + page_text
    except Exception as e:
        print(f"[WARN] Could not read PDF text: {e}")

    text_upper = text.upper()

    for bank, patterns in BANK_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text_upper, flags=re.I):
                return bank

    return "UNKNOWN"
