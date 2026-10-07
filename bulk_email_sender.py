import csv
import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER = "your_email@gmail.com"
APP_PASSWORD = "your_gmail_app_password"

TEMPLATE = """Dear {name},

This is a reminder that your {subject} record must be submitted on or before {due_date}. Please bring the printed record to the lab.

Regards,
BPA Lab Automation Bot
"""


def send_mails(csv_file):
    with open(csv_file, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER, APP_PASSWORD)
        print(f"Connected and logged in to {SMTP_SERVER}\n")

        for i, row in enumerate(rows, 1):
            msg = EmailMessage()
            msg["From"] = f"BPA Lab Bot <{SENDER}>"
            msg["To"] = row["email"]
            msg["Subject"] = f"Reminder: {row['subject']} Record Submission"
            msg.set_content(TEMPLATE.format(**row))
            server.send_message(msg)
            print(f"[{i}/{len(rows)}] Mail sent to {row['name']:<10}<{row['email']}>")

    print("\nAll reminder mails sent successfully!")


if __name__ == "__main__":
    send_mails("recipients.csv")
