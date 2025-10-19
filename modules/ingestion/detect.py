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
    ],
}

def detect_bank(pdf_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for pg in pdf.pages[:2]:
                t = (pg.extract_text() or "")
                text += "\n" + t
    except Exception:
        pass

    for bank, pats in BANK_PATTERNS.items():
        for pat in pats:
            if re.search(pat, text, flags=re.I):
                return bank
    return "UNKNOWN"
