import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_init = '''        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            logo TEXT,
            phone TEXT,
            contact_person TEXT,
            cr_number TEXT,
            industry TEXT,
            language TEXT,
            subscription_type TEXT
        )'''

new_init = '''        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            logo TEXT,
            phone TEXT,
            contact_person TEXT,
            cr_number TEXT,
            industry TEXT,
            language TEXT,
            subscription_type TEXT,
            status TEXT DEFAULT 'Active',
            portals TEXT DEFAULT 'Both',
            expiry_date TEXT,
            report_times TEXT DEFAULT '09:00,11:00,13:00,15:00'
        )'''

code = code.replace(old_init, new_init)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
