import glob
import os
import re

import pandas as pd
import pdfplumber

INVOICE_DIR = "invoices"
OUT = "invoice_summary.xlsx"


def amount_after(label, text):
    match = re.search(rf"{label}[^\n]*?([\d,]+(?:\.\d+)?)\s*$", text, re.I | re.M)
    return float(match.group(1).replace(",", "")) if match else 0.0


def text_after(label, text):
    match = re.search(rf"{label}\s*[:\-]?\s*(.+)", text, re.I)
    return match.group(1).strip() if match else ""


def extract_invoice(path):
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    invoice_no = re.search(r"Invoice\s*No\.?\s*[:\-]?\s*(\S+)", text, re.I)
    date = re.search(r"(\d{2}-\d{2}-\d{4})", text)
    return {
        "Invoice No": invoice_no.group(1) if invoice_no else "",
        "Date": date.group(1) if date else "",
        "Vendor": text_after("Vendor", text),
        "Bill To": text_after("Bill To", text),
        "Subtotal": amount_after(r"Sub\s*Total", text),
        "GST": amount_after("GST", text),
        "Grand Total": amount_after("Grand Total", text),
    }


records = []
for path in sorted(glob.glob(os.path.join(INVOICE_DIR, "*.pdf"))):
    record = extract_invoice(path)
    records.append(record)
    file = os.path.basename(path)
    print(f"Extracted {file:<14} | {record['Invoice No']} | {record['Vendor']:<22} | Rs. {record['Grand Total']:>9.2f}")

df = pd.DataFrame(records)
df.to_excel(OUT, index=False)
print(f"\nInvoices processed : {len(df)}")
print(f"Total amount       : Rs. {df['Grand Total'].sum():.2f}")
print(f"Saved to {OUT}")
