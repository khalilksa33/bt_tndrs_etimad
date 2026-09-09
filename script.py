import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

admin_add_pattern = r"def admin_add\(\):.*?except sqlite3\.IntegrityError:"
new_admin_add = '''def admin_add():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        contact = request.form.get('contact_person', '')
        cr = request.form.get('cr_number', '')
        industry = request.form.get('industry', '')
        language = request.form.get('language', 'English')
        sub_type = request.form.get('subscription_type', 'Monthly')
        status = request.form.get('status', 'Active')
        portals = request.form.get('portals', 'Both')
        expiry_date = request.form.get('expiry_date', '')
        report_times = ','.join(request.form.getlist('report_times')) or '09:00,11:00,13:00,15:00'
        
        conn = get_db()
        try:
            conn.execute(\'''
                INSERT INTO companies 
                (name, email, phone, contact_person, cr_number, industry, language, subscription_type, status, portals, expiry_date, report_times) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            \''', (name, email, phone, contact, cr, industry, language, sub_type, status, portals, expiry_date, report_times))
            conn.commit()
            
        except sqlite3.IntegrityError:'''

code = re.sub(admin_add_pattern, new_admin_add, code, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
