with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("company=company)", "company=dict(company) if company else None)")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
