import re

with open('etimad_tenders.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('"https://tenders.etimad.sa/ar/Tender/AllTendersForVisitor"', '"https://tenders.etimad.sa/Tender/AllTendersForVisitor"')

if "'--lang=ar'" not in code:
    code = code.replace("chrome_options.add_argument('--disable-dev-shm-usage')", "chrome_options.add_argument('--disable-dev-shm-usage')\n    chrome_options.add_argument('--lang=ar')")

with open('etimad_tenders.py', 'w', encoding='utf-8') as f:
    f.write(code)
