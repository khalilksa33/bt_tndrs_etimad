pdf_logic = r'''
def render_arabic(text):
    if not text: return text
    text_str = str(text)
    if not any('\u0600' <= c <= '\u06FF' for c in text_str):
        return text_str
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped_text = arabic_reshaper.reshape(text_str)
        return get_display(reshaped_text)
    except:
        return text_str

def draw_page_header(canvas_obj, doc, company_name=None, logo_path=None):
    from reportlab.lib.units import mm
    from reportlab.platypus import Image
    import os
    width, height = doc.pagesize
    top_y = height - 16 * mm
    if logo_path and os.path.exists(logo_path):
        img = Image(logo_path)
        img.drawHeight = 15 * mm
        img.drawWidth = (img.drawHeight / img.imageHeight) * img.imageWidth
        img.drawOn(canvas_obj, width - doc.rightMargin - img.drawWidth, top_y - img.drawHeight)
    if company_name:
        canvas_obj.saveState()
        canvas_obj.setFont("Amiri", 12)
        canvas_obj.drawString(doc.leftMargin, top_y, render_arabic("Report for: " + company_name))
        canvas_obj.restoreState()

def add_footer(canvas_obj, doc):
    from reportlab.lib.units import mm
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 8)
    footer_text = f"Page {doc.page}"
    canvas_obj.drawCentredString(doc.pagesize[0] / 2.0, 10 * mm, footer_text)
    canvas_obj.restoreState()

def build_pdf(rows, path, company_name=None, logo_path=None):
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    from reportlab.lib.units import mm
    import os

    try:
        pdfmetrics.registerFont(TTFont('Amiri', 'Amiri-Regular.ttf'))
        font_name = 'Amiri'
    except Exception as e:
        print("Font error:", e)
        font_name = 'Helvetica'

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'reportTitle',
        parent=styles['Title'],
        alignment=1,
        fontName=font_name,
        fontSize=14,
        leading=16,
        spaceAfter=4 * mm,
    )
    
    story = []
    title_text = render_arabic("Automated Tenders Report")
    story.append(Paragraph(title_text, title_style))
    story.append(Spacer(1, 10 * mm))

    headers = [
        "Title", "Publisher", "Type", "Activity", "Category", 
        "Ref Value", "Publish Date", "Inquiry Date", 
        "Submit Date", "Opening Date", "Price"
    ]
    if rows and any('\u0600' <= c <= '\u06FF' for cell in rows[0] for c in str(cell)):
        headers = [
            "العنوان", "الناشر", "النوع", "النشاط", "التصنيف",
            "القيمة المرجعية", "تاريخ النشر", "اخر موعد للاستفسارات",
            "اخر موعد للتقديم", "تاريخ فتح المظاريف", "قيمة الكراسة"
        ]

    rendered_headers = [Paragraph(render_arabic(h), ParagraphStyle('h', fontName=font_name, fontSize=8, textColor=colors.white)) for h in headers]
    data = [rendered_headers]
    
    for i, row in enumerate(rows, start=1):
        rendered_row = []
        for cell in row:
            rendered_row.append(Paragraph(render_arabic(cell), ParagraphStyle('c', fontName=font_name, fontSize=7)))
        data.append(rendered_row)

    col_widths = [50*mm, 30*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 15*mm]
    table = Table(data, colWidths=col_widths[:len(headers)], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#B91C1C")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
    ]))
    story.append(table)

    doc = SimpleDocTemplate(
        path,
        pagesize=landscape(A4),
        rightMargin=10*mm,
        leftMargin=10*mm,
        topMargin=20*mm,
        bottomMargin=15*mm
    )
    
    doc.build(story, 
              onFirstPage=lambda canvas_obj, doc: (draw_page_header(canvas_obj, doc, company_name, logo_path), add_footer(canvas_obj, doc)),
              onLaterPages=lambda canvas_obj, doc: (draw_page_header(canvas_obj, doc, company_name, logo_path), add_footer(canvas_obj, doc)))

'''

for filename in ['forsah_tenders.py', 'etimad_tenders.py']:
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()

    start_idx = code.find('def draw_page_header')
    if start_idx == -1:
        start_idx = code.find('def build_pdf')
    
    end_idx = code.find('def main(')
    
    if start_idx != -1 and end_idx != -1:
        code = code[:start_idx] + pdf_logic + '\n' + code[end_idx:]
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code)

