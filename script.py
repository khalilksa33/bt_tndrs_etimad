import re

with open('etimad_tenders.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('"https://tenders.etimad.sa/Tender/AllTendersForVisitor"', '"https://tenders.etimad.sa/ar/Tender/AllTendersForVisitor"')

with open('etimad_tenders.py', 'w', encoding='utf-8') as f:
    f.write(code)
