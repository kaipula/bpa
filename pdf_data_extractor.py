import csv
import re
import pdfplumber

PDF_FILE = "student_form.pdf"

FIELDS = {
    "Name": r"Name\s*:\s*(.+)",
    "Register No": r"Register No\s*:\s*(\S+)",
    "Email": r"Email\s*:\s*(\S+@\S+)",
    "Phone": r"Phone\s*:\s*(\d{10})",
    "Date": r"Date\s*:\s*(\d{2}-\d{2}-\d{4})",
}

with pdfplumber.open(PDF_FILE) as pdf:
    print(f"{'File':<11}: {PDF_FILE}")
    print(f"Total pages: {len(pdf.pages)}")

    text = ""
    tables = []
    for page in pdf.pages:
        text += (page.extract_text() or "") + "\n"
        tables.extend(page.extract_tables())

print("\n----- Extracted Text -----")
print(text.strip())

print("\n----- Extracted Fields -----")
for label, pattern in FIELDS.items():
    match = re.search(pattern, text)
    value = match.group(1).strip() if match else "Not found"
    print(f"{label:<12}: {value}")

if tables:
    with open("courses.csv", "w", newline="") as f:
        csv.writer(f).writerows(tables[0])
    print(f"\nTable with {len(tables[0]) - 1} rows saved to courses.csv")
else:
    print("\nNo table found in the PDF")
