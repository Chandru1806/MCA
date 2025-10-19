import os
import uuid
import traceback
import pandas as pd
from flask import (
    current_app, render_template, request, send_from_directory,
    redirect, url_for, send_file, flash
)
from werkzeug.utils import secure_filename
from . import ingestion_bp
from .detect import detect_bank
from .extract import parse_kotak_df, parse_hdfc_df, parse_generic_df
from .standardize import standardize_and_write
from modules.repair.repair_rejects import repair_reject_file

# Golden STD schema
STD_COLS = [
    "Transaction_ID",
    "Transaction_Date",
    "Description",
    "Debit_Amount",
    "Credit_Amount",
    "Balance",
    "Bank_Name",
]

def _is_pdf_filename(name: str) -> bool:
    return (name or "").lower().endswith(".pdf")

# ----------------------------
# Ingestion Routes
# ----------------------------

@ingestion_bp.get("/ingestion")
def index():
    return render_template("ingestion/upload.html")

@ingestion_bp.post("/ingestion/upload")
def upload():
    """
    Unified upload for PDFs and/or CSVs.
    - PDFs: parse & standardize
    - CSVs: merge into one file
    """
    upload_dir = current_app.config.get("UPLOAD_FOLDER", "storage/uploads")
    output_dir = current_app.config.get("OUTPUT_FOLDER", "storage/outputs")
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    bank_hint = (request.form.get("bank") or "").strip() or None

    # Collect both PDFs and CSVs
    pdf_files = request.files.getlist("pdfs")
    csv_files = request.files.getlist("csv_files")

    # Nothing selected?
    if (not pdf_files or all((f.filename or "").strip() == "" for f in pdf_files)) \
       and (not csv_files or all((f.filename or "").strip() == "" for f in csv_files)):
        return "No files selected.", 400

    batch_id = str(uuid.uuid4())[:8]
    std_csvs, rej_csvs = [], []
    merged_df = pd.DataFrame()

    # --- Process PDFs ---
    for f in pdf_files:
        raw_name = (f.filename or "").strip()
        if not raw_name or not _is_pdf_filename(raw_name):
            continue

        safe = secure_filename(raw_name)
        in_path = os.path.join(upload_dir, f"{batch_id}_{safe}")
        f.save(in_path)

        bank = bank_hint or detect_bank(in_path)
        base = os.path.splitext(os.path.basename(in_path))[0]

        try:
            if bank == "KOTAK":
                df_raw = parse_kotak_df(in_path)
            elif bank == "HDFC":
                df_raw = parse_hdfc_df(in_path)
            else:
                df_raw = parse_generic_df(in_path)

            std_csv, rej_csv = standardize_and_write(df_raw, bank, base, output_dir)
            std_csvs.append(os.path.basename(std_csv))
            rej_csvs.append(os.path.basename(rej_csv))

        except Exception as e:
            err_bank = (bank or "UNKNOWN").upper()
            std_path = os.path.join(output_dir, f"{base}__STD_{err_bank}.csv")
            rej_path = os.path.join(output_dir, f"{base}__REJECTS_{err_bank}.csv")

            pd.DataFrame(columns=STD_COLS).to_csv(std_path, index=False, encoding="utf-8-sig")
            tb = traceback.format_exc(limit=2)
            rej_df = pd.DataFrame([{
                "Bank_Name": err_bank,
                "Raw_Date": "",
                "Raw_Narration": "",
                "Raw_Debit": "",
                "Raw_Credit": "",
                "Raw_Balance": "",
                "Reason": "parser_exception",
                "Detail": str(e),
                "Trace": tb,
            }])
            rej_df.to_csv(rej_path, index=False, encoding="utf-8-sig")

            std_csvs.append(os.path.basename(std_path))
            rej_csvs.append(os.path.basename(rej_path))

    # --- Process CSVs ---
    for f in csv_files:
        raw_name = (f.filename or "").strip()
        if raw_name.lower().endswith(".csv"):
            safe = secure_filename(raw_name)
            in_path = os.path.join(upload_dir, f"{batch_id}_{safe}")
            f.save(in_path)
            try:
                df = pd.read_csv(in_path)
                df["Source_File"] = raw_name
                merged_df = pd.concat([merged_df, df], ignore_index=True)
            except Exception as e:
                print(f"❌ Failed to read CSV: {raw_name} — {e}")

    merged_name = None
    if not merged_df.empty:
        merged_path = os.path.join(output_dir, "merged_transactions.csv")
        merged_df.to_csv(merged_path, index=False)
        merged_name = "merged_transactions.csv"
        std_csvs.append(merged_name)

    if not std_csvs:
        return "No valid files processed.", 400

    return redirect(url_for(
        "ingestion.preview",
        primary=std_csvs[0],
        others=",".join(std_csvs[1:]),
        rejects=",".join(rej_csvs)
    ))

@ingestion_bp.get("/ingestion/preview")
def preview():
    primary = request.args.get("primary")
    others  = [x for x in (request.args.get("others") or "").split(",") if x]
    rejects = [x for x in (request.args.get("rejects") or "").split(",") if x]
    return render_template("ingestion/preview.html", primary=primary, others=others, rejects=rejects)

@ingestion_bp.get("/ingestion/download/<path:fname>")
def download(fname):
    output_dir = current_app.config.get("OUTPUT_FOLDER", "storage/outputs")
    return send_from_directory(output_dir, fname, as_attachment=True)

# ----------------------------
# Repair Rejects Route
# ----------------------------

@ingestion_bp.route("/repair", methods=["GET", "POST"])
def repair():
    supported_banks = ["HDFC", "KOTAK", "CUB", "ICICI", "SBI", "AXIS", "IDFC"]

    if request.method == "POST":
        file = request.files.get("reject_file")
        bank = request.form.get("bank")

        if not file or not bank:
            flash("Missing file or bank.")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        upload_path = os.path.join("storage", "uploads", filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        print(f"📥 Uploaded reject file: {upload_path}")

        try:
            repaired_df = repair_reject_file(upload_path, bank)
        except Exception as e:
            print(f"❌ Error during repair: {e}")
            flash("Repair failed with an exception.")
            return redirect(request.url)

        if repaired_df is not None and not repaired_df.empty:
            output_path = upload_path.replace("__REJECTS_", "__RECOVERED_")
            print(f"✅ Sending repaired file: {output_path}")
            return send_file(output_path, as_attachment=True)
        else:
            print("⚠️ Repair returned empty or None.")
            flash("Repair failed or file was empty or incorrect format.")
            return redirect(request.url)

    return render_template("repair.html", banks=supported_banks)
