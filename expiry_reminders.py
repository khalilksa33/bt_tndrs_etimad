import sqlite3
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tenders.db')

def get_settings():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("SELECT * FROM settings").fetchall()
        settings = {row['key']: row['value'] for row in rows}
    except sqlite3.OperationalError:
        settings = {}
    conn.close()
    return settings

def send_reminder(company, days_left, settings):
    SMTP_HOST = settings.get("smtp_host") or os.environ.get("SMTP_HOST")
    SMTP_PORT = int(settings.get("smtp_port") or os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = settings.get("smtp_user") or os.environ.get("SMTP_USER")
    SMTP_PASS = settings.get("smtp_pass") or os.environ.get("SMTP_PASS")
    EMAIL_FROM = settings.get("email_from") or os.environ.get("EMAIL_FROM", SMTP_USER)
    
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, company['email']]):
        print(f"Skipping {company['email']}: Missing SMTP settings.")
        return

    msg = MIMEMultipart()
    msg['From'] = f"TendersHub <{EMAIL_FROM}>"
    msg['To'] = company['email']
    
    if days_left > 0:
        msg['Subject'] = f"TendersHub: Your subscription expires in {days_left} days"
        body = f"Dear {company['name']},\n\nThis is a friendly reminder that your TendersHub subscription will expire on {company['expiry_date']}.\nPlease renew your subscription to avoid any interruption in receiving your daily tenders.\n\nThank you,\nTendersHub Team"
    else:
        msg['Subject'] = "TendersHub: Your subscription has expired"
        body = f"Dear {company['name']},\n\nYour TendersHub subscription expired today ({company['expiry_date']}).\nYour account has been suspended and you will no longer receive daily tender reports until you renew.\n\nThank you,\nTendersHub Team"

    msg.attach(MIMEText(body, 'plain'))

    try:
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
        print(f"Sent reminder to {company['email']}")
    except Exception as e:
        print(f"Failed to send reminder to {company['email']}: {e}")

def main():
    settings = get_settings()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        companies = conn.execute("SELECT * FROM companies WHERE status = 'Active' AND expiry_date != '' AND expiry_date IS NOT NULL").fetchall()
    except sqlite3.OperationalError:
        companies = []
    
    today = datetime.now().date()
    for company in companies:
        try:
            exp_date = datetime.strptime(company['expiry_date'], "%Y-%m-%d").date()
            days_left = (exp_date - today).days
            
            if days_left == 3 or days_left == 0:
                send_reminder(company, days_left, settings)
                
                # Auto-suspend if expired today
                if days_left == 0:
                    conn.execute("UPDATE companies SET status = 'Suspended' WHERE id = ?", (company['id'],))
        except ValueError:
            continue
            
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
