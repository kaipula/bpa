import os
import shutil
import logging
from datetime import datetime

SOURCE = "Downloads_Demo"

CATEGORIES = {
    "Documents": [".pdf", ".docx", ".txt"],
    "Code": [".py", ".java"],
    "Spreadsheets": [".csv", ".xlsx"],
    "Images": [".jpg", ".png"],
    "Archives": [".zip"],
}

logging.basicConfig(
    filename="file_manager.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def create_sample_files():
    os.makedirs(SOURCE, exist_ok=True)
    samples = [
        "HCI_Notes.pdf", "Resume.docx", "todo.txt",
        "main.py", "Library.java",
        "attendance.csv", "marks.xlsx",
        "photo1.jpg", "screenshot.png",
        "project_backup.zip", "unknown.xyz",
    ]
    for name in samples:
        open(os.path.join(SOURCE, name), "w").close()
    print(f"Created {len(samples)} sample files in '{SOURCE}'\n")


def get_category(ext):
    for category, extensions in CATEGORIES.items():
        if ext.lower() in extensions:
            return category
    return "Others"


def organize(folder):
    summary = {}
    stamp = datetime.now().strftime("%Y%m%d")
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            continue
        category = get_category(os.path.splitext(name)[1])
        os.makedirs(os.path.join(folder, category), exist_ok=True)
        new_name = f"{stamp}_{name}"
        shutil.move(path, os.path.join(folder, category, new_name))
        logging.info(f"Moved {name} -> {category}/{new_name}")
        print(f"Moved: {name:<20} -> {category}/{new_name}")
        summary[category] = summary.get(category, 0) + 1
    return summary


if __name__ == "__main__":
    create_sample_files()
    result = organize(SOURCE)
    print("\n----- Summary -----")
    for category, count in result.items():
        print(f"{category:<14}: {count} file(s)")
    print(f"Total organised : {sum(result.values())}")
    print("Log written to file_manager.log")
