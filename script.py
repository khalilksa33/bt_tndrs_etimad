import re

with open('forsah_tenders.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_lang_check = '''pdf_rows = arabic_rows if c_lang == "Arabic" else english_rows'''
new_lang_check = '''pdf_rows = arabic_rows if c_lang in ["Arabic", "العربية"] else english_rows'''

code = code.replace(old_lang_check, new_lang_check)

with open('forsah_tenders.py', 'w', encoding='utf-8') as f:
    f.write(code)
