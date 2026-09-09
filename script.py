import re

with open('etimad_tenders.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_opts = '''    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")'''

new_opts = '''    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")'''

code = code.replace(old_opts, new_opts)

with open('etimad_tenders.py', 'w', encoding='utf-8') as f:
    f.write(code)
