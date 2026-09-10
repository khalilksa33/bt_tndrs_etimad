import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Update Add form in admin
old_admin_add = '''<label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Report Schedule (Hold Ctrl/Cmd to select multiple)</label>
                                <select name="report_times" multiple class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-2 h-24">
                                    <option value="09:00" selected>09:00 AM</option>
                                    <option value="11:00" selected>11:00 AM</option>
                                    <option value="13:00" selected>01:00 PM</option>
                                    <option value="15:00" selected>03:00 PM</option>
                                    <option value="17:00">05:00 PM</option>
                                    <option value="19:00">07:00 PM</option>
                                </select>'''

new_admin_add = '''<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Report Schedule</label>
                                <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="09:00" checked class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">09:00 AM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="11:00" checked class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">11:00 AM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="13:00" checked class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">01:00 PM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="15:00" checked class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">03:00 PM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="17:00" class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">05:00 PM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="19:00" class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">07:00 PM</span></label>
                                </div>'''
code = code.replace(old_admin_add, new_admin_add)

# Update Edit form in admin
old_admin_edit = '''<label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Report Schedule (Hold Ctrl/Cmd to select multiple)</label>
                                <select name="report_times" multiple class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-2 h-24">
                                    {% set times = company.get('report_times', '09:00,11:00,13:00,15:00').split(',') %}
                                    <option value="09:00" {% if '09:00' in times %}selected{% endif %}>09:00 AM</option>
                                    <option value="11:00" {% if '11:00' in times %}selected{% endif %}>11:00 AM</option>
                                    <option value="13:00" {% if '13:00' in times %}selected{% endif %}>01:00 PM</option>
                                    <option value="15:00" {% if '15:00' in times %}selected{% endif %}>03:00 PM</option>
                                    <option value="17:00" {% if '17:00' in times %}selected{% endif %}>05:00 PM</option>
                                    <option value="19:00" {% if '19:00' in times %}selected{% endif %}>07:00 PM</option>
                                </select>'''

new_admin_edit = '''<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Report Schedule</label>
                                <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                                    {% set times = company.get('report_times', '09:00,11:00,13:00,15:00').split(',') if company else [] %}
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="09:00" {% if '09:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">09:00 AM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="11:00" {% if '11:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">11:00 AM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="13:00" {% if '13:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">01:00 PM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="15:00" {% if '15:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">03:00 PM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="17:00" {% if '17:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">05:00 PM</span></label>
                                    <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="19:00" {% if '19:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">07:00 PM</span></label>
                                </div>'''
code = code.replace(old_admin_edit, new_admin_edit)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
