import re

with open('.github/workflows/deploy.yml', 'r', encoding='utf-8') as f:
    code = f.read()

old_cron = '''          (echo "0 9,11,13,15 * * * cd ~/bt_tndrs_etimad && ~/bt_tndrs_etimad/venv/bin/python3 ~/bt_tndrs_etimad/forsah_tenders.py >> ~/bt_tndrs_etimad/bt_etmd_tndrs_cron.log 2>&1"; echo "0 9,11,13,15 * * * cd ~/bt_tndrs_etimad && ~/bt_tndrs_etimad/venv/bin/python3 ~/bt_tndrs_etimad/etimad_tenders.py >> ~/bt_tndrs_etimad/etimad_tenders_cron.log 2>&1"; echo "0 10 * * * cd ~/bt_tndrs_etimad && ~/bt_tndrs_etimad/venv/bin/python3 ~/bt_tndrs_etimad/expiry_reminders.py >> ~/bt_tndrs_etimad/expiry_reminders.log 2>&1") | crontab -'''
new_cron = '''          (echo "0 * * * * cd ~/bt_tndrs_etimad && ~/bt_tndrs_etimad/venv/bin/python3 ~/bt_tndrs_etimad/forsah_tenders.py >> ~/bt_tndrs_etimad/bt_etmd_tndrs_cron.log 2>&1"; echo "0 * * * * cd ~/bt_tndrs_etimad && ~/bt_tndrs_etimad/venv/bin/python3 ~/bt_tndrs_etimad/etimad_tenders.py >> ~/bt_tndrs_etimad/etimad_tenders_cron.log 2>&1"; echo "0 10 * * * cd ~/bt_tndrs_etimad && ~/bt_tndrs_etimad/venv/bin/python3 ~/bt_tndrs_etimad/expiry_reminders.py >> ~/bt_tndrs_etimad/expiry_reminders.log 2>&1") | crontab -'''

code = code.replace(old_cron, new_cron)

with open('.github/workflows/deploy.yml', 'w', encoding='utf-8') as f:
    f.write(code)
