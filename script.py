import re

with open('etimad_tenders.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("card.text.split('\\n')", "card.text.split('\\n')")
code = code.replace("card.text.split('\n')", "card.text.split('\\n')")

with open('etimad_tenders.py', 'w', encoding='utf-8') as f:
    f.write(code)
