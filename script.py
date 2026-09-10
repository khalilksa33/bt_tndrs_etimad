import re
with open('etimad_tenders.py', 'r', encoding='utf-8') as f: code = f.read()
code = code.replace("ChromeDriverManager().install()", "ChromeDriverManager(driver_version='152.0.7977.64').install()")
with open('etimad_tenders.py', 'w', encoding='utf-8') as f: f.write(code)
