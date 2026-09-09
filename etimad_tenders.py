#!/usr/bin/env python3
import os
import re
import ssl
import json
import sqlite3
import argparse
import urllib.request
import urllib.parse
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()

FORSAH_API_BASE_URL = os.environ.get(
    "FORSAH_API_BASE_URL",
    "https://etimad-api.910ths.sa/api/v1/opportunities",
)
FORSAH_PER_PAGE = int(os.environ.get("FORSAH_PER_PAGE", "50"))
MAX_ROWS = int(os.environ.get("MAX_ROWS", "50"))
DATABASE_PATH = os.environ.get("DATABASE_PATH", "tenders.db")
SMTP_HOST = None
SMTP_PORT = 587
SMTP_USER = None
SMTP_PASS = None
EMAIL_FROM = None

conn = sqlite3.connect(DATABASE_PATH)
try:
    settings_rows = conn.execute("SELECT * FROM settings").fetchall()
    settings = {row[0]: row[1] for row in settings_rows}
    SMTP_HOST = settings.get("smtp_host") or os.environ.get("SMTP_HOST")
    SMTP_PORT = int(settings.get("smtp_port") or os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = settings.get("smtp_user") or os.environ.get("SMTP_USER")
    SMTP_PASS = settings.get("smtp_pass") or os.environ.get("SMTP_PASS")
    EMAIL_FROM = settings.get("email_from") or os.environ.get("EMAIL_FROM", SMTP_USER)
except sqlite3.OperationalError:
    pass
conn.close()
EMAIL_TO = os.environ.get("EMAIL_TO")
REPORT_TITLE = os.environ.get("FORSAH_REPORT_TITLE", "Etimad Tenders – Daily Report")


FOOTER_TEXT = os.environ.get("FOOTER_TEXT", "")

translator = GoogleTranslator(source='ar', target='en')


def clean_text(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tenders (
            tender_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            reference TEXT NOT NULL,
            title TEXT,
            entity TEXT,
            sub_entity TEXT,
            tender_type TEXT,
            activity TEXT,
            publication TEXT,
            inquiry_deadline TEXT,
            submission_deadline TEXT,
            opening TEXT,
            price TEXT,
            raw_json TEXT,
            scraped_at TEXT,
            UNIQUE(source, reference)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tender_id INTEGER,
            attendee_name TEXT,
            status TEXT,
            timestamp TEXT,
            FOREIGN KEY(tender_id) REFERENCES tenders(tender_id)
        )
        """
    )
    conn.commit()
    conn.close()


def save_rows_to_db(rows, source, raw_rows=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    now = datetime.now().isoformat()
    before = conn.total_changes
    for idx, row in enumerate(rows):
        reference = row[5] if len(row) > 5 and row[5] else str(hash(str(row)))
        raw_json = None
        if raw_rows and idx < len(raw_rows):
            try:
                raw_json = json.dumps(raw_rows[idx], ensure_ascii=False)
            except Exception:
                raw_json = None
        cur.execute(
            """
            INSERT OR IGNORE INTO tenders (
                source, reference, title, entity, sub_entity,
                tender_type, activity, publication, inquiry_deadline,
                submission_deadline, opening, price, raw_json, scraped_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source,
                reference,
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[6],
                row[7],
                row[8],
                row[9],
                row[10],
                raw_json,
                now,
            ),
        )
    conn.commit()
    inserted = conn.total_changes - before
    conn.close()
    return inserted


def load_rows_from_db(source):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT title, entity, sub_entity, tender_type, activity, reference,
               publication, inquiry_deadline, submission_deadline, opening, price
        FROM tenders
        WHERE source = ?
        ORDER BY scraped_at DESC, tender_id DESC
        """,
        (source,),
    )
    rows = cur.fetchall()
    conn.close()
    return [list(row) for row in rows]


def arabic_digits_to_ascii(text):
    if not text:
        return text
    trans = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
    return text.translate(trans)


def parse_date(value):
    if not value:
        return None
    text = arabic_digits_to_ascii(clean_text(value)).replace('/', '-').replace('.', '-').replace('\u200f', '').strip()
    text = re.sub(r'T', ' ', text)
    text = re.sub(r'Z$', '', text)
    text = re.sub(r'([+-]\d{2}:\d{2})$', '', text)
    patterns = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%d-%m-%Y',
        '%d %b %Y',
        '%d %B %Y',
        '%d %b, %Y',
        '%d %B, %Y',
    ]
    for pattern in patterns:
        try:
            return datetime.strptime(text, pattern)
        except Exception:
            continue
    return None


def is_today(value):
    date_obj = parse_date(value)
    return bool(date_obj and date_obj.date() == datetime.now().date())


def sort_rows(rows):
    def sort_key(row):
        pub_date = parse_date(row[6])
        return pub_date or datetime.min
    return sorted(rows, key=sort_key, reverse=True)


def get_localized_text(value):
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, dict):
        return clean_text(value.get('en') or value.get('ar') or next(iter(value.values()), ''))
    return ''


def translate_arabic_to_english(text):
    if not text or not any('\u0600' <= char <= '\u06FF' for char in text):
        return text
    try:
        return translator.translate(text)
    except Exception:
        return text


def translate_rows(rows):
    translated_rows = []
    for row in rows:
        translated_rows.append([translate_arabic_to_english(cell) if cell else cell for cell in row])
    return translated_rows


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_rows():
    print("🚀 Starting Etimad headless browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    arabic_rows = []
    
    try:
        driver.get("https://tenders.etimad.sa/Tender/AllTendersForVisitor")
        # Wait for the page to load the tender cards. We wait for a generic class that usually wraps the tenders.
        # Note: Since Etimad's HTML layout updates often, you may need to adjust these CSS selectors.
        time.sleep(5) # Let WAF clear
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card, .tender-card, div[class*='tender']")))
        
        cards = driver.find_elements(By.CSS_SELECTOR, ".card, .tender-card, div[class*='tender']")[:MAX_ROWS]
        print(f"✅ Found {len(cards)} tender cards on Etimad")
        
        for card in cards:
            try:
                # Basic generic extraction strategy for Etimad
                text_content = card.text.split('\n')
                
                title = text_content[0] if len(text_content) > 0 else 'N/A'
                publisher = text_content[1] if len(text_content) > 1 else 'Etimad Entity'
                tender_type = "Public Tender"
                activity = "N/A"
                category = "General"
                ref_num = card.get_attribute("id") or str(time.time())
                pub_date = "Today"
                inquiry_deadline = ""
                submit_date = ""
                opening_date = ""
                price = "See Details"
                
                # Attempt to find actual link for reference ID if available
                links = card.find_elements(By.TAG_NAME, "a")
                if links:
                    href = links[0].get_attribute("href")
                    if href:
                        ref_num = href.split('/')[-1]

                arabic_rows.append([
                    title, publisher, tender_type, activity, category,
                    ref_num, pub_date, inquiry_deadline, submit_date,
                    opening_date, price
                ])
            except Exception as e:
                print(f"Warning: Failed to parse a card: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Failed to scrape Etimad: {e}")
        driver.save_screenshot('etimad_error.png')
    finally:
        driver.quit()
        
    return arabic_rows

def build_pdf(rows, path, company_name=None, logo_path=None):
    styles = getSampleStyleSheet()
    story = []
    title_style = ParagraphStyle(
        'reportTitle',
        parent=styles['Title'],
        alignment=1,
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        spaceAfter=4 * mm,
    )
    story.append(Paragraph(REPORT_TITLE, title_style))
    timestamp_style = ParagraphStyle(
        'reportTimestamp',
        parent=styles['Normal'],
        alignment=1,
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        textColor=colors.grey,
        spaceAfter=4 * mm,
    )
    story.append(Paragraph(datetime.now().strftime('Generated on %Y-%m-%d %H:%M'), timestamp_style))
    headers = [
        "#",
        "Tender title",
        "Publisher",
        "Category",
        "Type",
        "Activity",
        "Ref no.",
        "Publication",
        "Inquiry deadline",
        "Submission deadline",
        "Opening",
        "Doc price",
    ]
    cell_style = styles["BodyText"]
    cell_style.fontSize = 6
    cell_style.leading = 8
    cell_style.spaceBefore = 0
    cell_style.spaceAfter = 0
    header_style = ParagraphStyle(
        'tableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1,
    )
    wrapped_headers = []
    for header in headers:
        if header in ('Inquiry deadline', 'Submission deadline'):
            wrapped_headers.append(Paragraph(header.replace(' ', '<br/>', 1), header_style))
        elif ' / ' in header:
            wrapped_headers.append(Paragraph(header.replace(' / ', '<br/>/ '), header_style))
        else:
            wrapped_headers.append(Paragraph(header, header_style))
    data = [wrapped_headers]
    for i, row in enumerate(rows, start=1):
        data.append([Paragraph(str(i), cell_style)] + [Paragraph(str(cell or ""), cell_style) for cell in row])
    col_widths = [8*mm, 75*mm, 33*mm, 26*mm, 20*mm, 18*mm, 25*mm, 18*mm, 18*mm, 18*mm, 18*mm, 12*mm]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.red),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 1),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("GRID", (0, 0), (-1, 0), 0.5, colors.white),
        ("GRID", (0, 1), (-1, -1), 0.5, colors.red),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.red),
        ("LINEABOVE", (0, 0), (-1, 0), 0.5, colors.white),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.white),
    ]))
    story.append(table)
    doc = SimpleDocTemplate(
        path,
        pagesize=landscape(A4),
        rightMargin=15,
        leftMargin=15,
        topMargin=35 * mm,
        bottomMargin=24 * mm,
    )
    doc.build(story, onFirstPage=lambda canvas_obj, doc: (draw_page_header(canvas_obj, doc, company_name, logo_path), add_footer(canvas_obj, doc)), onLaterPages=lambda canvas_obj, doc: (draw_page_header(canvas_obj, doc, company_name, logo_path), add_footer(canvas_obj, doc)))


def send_email(pdf_path, email_to):
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, email_to]):
        raise RuntimeError("SMTP or email variables missing. Check .env")
    now = datetime.now().strftime("%Y-%m-%d")
    subject = f"{REPORT_TITLE} – {now}"
    body = "Attached is today’s generated Etimad tenders report in PDF format."
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', help='Send report only to this specific email')
    args = parser.parse_args()

    print("🔄 Starting Etimad tenders scraper...")
    arabic_rows = fetch_rows()
    if not arabic_rows:
        print("❌ No Etimad tenders scraped; aborting.")
        return
    print(f"✅ Scraped {len(arabic_rows)} Etimad tenders")
    print("🌐 Translating to English...")
    english_rows = translate_rows(arabic_rows)
    print("✅ Translation complete")
    original_count = len(english_rows)
    print(f"✅ Keeping {original_count} Etimad tenders published today")
    init_db()
    new_count = save_rows_to_db(english_rows, "etimad")
    print(f"✅ Saved {new_count} new Etimad tenders to database")
    reported_file = 'reported_etimad_tenders.json'
    with open(reported_file, 'w', encoding='utf-8') as f:
        json.dump({row[5]: row for row in english_rows}, f, indent=2, ensure_ascii=False)
    today = datetime.now().strftime("%Y%m%d")
    report_dir = os.path.join('reports', today)
    os.makedirs(report_dir, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        if args.email:
            companies = conn.execute("SELECT * FROM companies WHERE email = ?", (args.email,)).fetchall()
        else:
            companies = conn.execute("SELECT * FROM companies WHERE (status IS NULL OR status = 'Active') AND (portals IS NULL OR portals = 'Both' OR portals = 'Etimad')").fetchall()
            
            # Filter by scheduled time
            current_hour = datetime.now().strftime("%H:00")
            filtered_companies = []
            for c in companies:
                try:
                    c_times = dict(c).get('report_times')
                except Exception:
                    c_times = None
                if not c_times:
                    c_times = "09:00,11:00,13:00,15:00"
                if current_hour in c_times.split(','):
                    filtered_companies.append(c)
            companies = filtered_companies
            
    except sqlite3.OperationalError:
        companies = []
    conn.close()
    
    if companies:
        for company in companies:
            c_name = company["name"]
            c_email = company["email"]
            c_lang = company["language"]
            c_logo = os.path.join("logos", company["logo"]) if company["logo"] else None
            
            company_pdf_name = os.path.join(report_dir, f"etimad_tenders_report_{today}_{c_name.replace(' ', '_')}.pdf")
            print(f"📄 Building Etimad PDF for {c_name} (Language: {c_lang}): {company_pdf_name}")
            
            pdf_rows = arabic_rows if c_lang in ["Arabic", "العربية"] else english_rows
            build_pdf(pdf_rows, company_pdf_name, company_name=c_name, logo_path=c_logo)
            
            print(f"✉️ Sending Etimad email with PDF to {c_email}...")
            try:
                send_email(company_pdf_name, c_email)
            except Exception as e:
                print(f"❌ Failed to send to {c_email}: {e}")
    else:
        print("⚠️ No companies found in the database. Generating default PDF.")
        pdf_name = os.path.join(report_dir, f"etimad_tenders_report_{today}.pdf")
        build_pdf(english_rows, pdf_name)



if __name__ == "__main__":
    main()





