import re

send_email_logic = '''def send_email(pdf_path, email_to):
    import smtplib
    import ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from datetime import datetime
    import os

    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, email_to]):
        raise RuntimeError("SMTP or email variables missing. Check .env")
    now = datetime.now().strftime("%Y-%m-%d")
    subject = f"{REPORT_TITLE} – {now}"
    body = "Attached is today’s generated tenders report in PDF format."
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    with open(pdf_path, "rb") as f:
        part = MIMEApplication(f.read(), _subtype="pdf")
        part.add_header("Content-Disposition", "attachment", filename=os.path.basename(pdf_path))
        msg.attach(part)
    context = ssl.create_default_context()
    if SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=30) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
'''

for filename in ['forsah_tenders.py', 'etimad_tenders.py']:
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()

    code = code.replace('def main(', send_email_logic + '\ndef main(')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code)

