import email
import imaplib
import os
from email.header import decode_header

IMAP_SERVER = "imap.gmail.com"
USER = "your_email@gmail.com"
APP_PASSWORD = "your_gmail_app_password"
SAVE_DIR = "attachments"
KEYWORD = "Invoice"

os.makedirs(SAVE_DIR, exist_ok=True)


def decode(value):
    if value is None:
        return ""
    parts = decode_header(value)
    return "".join(
        p.decode(enc or "utf-8", errors="replace") if isinstance(p, bytes) else p
        for p, enc in parts
    )


mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(USER, APP_PASSWORD)
mail.select("INBOX")
print(f"Logged in to {IMAP_SERVER} - INBOX selected")

status, data = mail.search(None, f'(UNSEEN SUBJECT "{KEYWORD}")')
ids = data[0].split()
print(f"Unread mails with '{KEYWORD}' in subject: {len(ids)}\n")

count = 0
for num in ids:
    status, msg_data = mail.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])

    print(f"From    : {decode(msg['From'])}")
    print(f"Subject : {decode(msg['Subject'])}")
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = decode(part.get_filename())
            with open(os.path.join(SAVE_DIR, filename), "wb") as f:
                f.write(part.get_payload(decode=True))
            count += 1
            print(f"  -> Downloaded: {filename}")
    print()

mail.logout()
print(f"{count} attachment(s) saved to '{SAVE_DIR}' folder")
