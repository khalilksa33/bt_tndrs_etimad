import re

for filename in ['forsah_tenders.py', 'etimad_tenders.py']:
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()

    # Add datetime timezone import if needed
    if 'from datetime import datetime, timedelta, timezone' not in code:
        code = code.replace('from datetime import datetime', 'from datetime import datetime, timedelta, timezone')

    # Replace datetime.now() with datetime.now(timezone(timedelta(hours=3)))
    code = code.replace('current_hour = datetime.now().strftime("%H:00")', 'current_hour = datetime.now(timezone(timedelta(hours=3))).strftime("%H:00")')
    code = code.replace("today = datetime.now().strftime('%Y-%m-%d')", "today = datetime.now(timezone(timedelta(hours=3))).strftime('%Y-%m-%d')")
    code = code.replace('datetime.now().strftime("%Y%m%d")', 'datetime.now(timezone(timedelta(hours=3))).strftime("%Y%m%d")')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code)
