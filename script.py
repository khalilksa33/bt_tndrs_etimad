import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'''                          <div>
                              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Subscription Type</label>
                              <select name="subscription_type" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-2">
                                  <option value="Monthly" {% if company and company\['subscription_type'\] == 'Monthly' %}selected{% endif %}>Monthly</option>
                                  <option value="Annual" {% if company and company\['subscription_type'\] == 'Annual' %}selected{% endif %}>Annual</option>
                              </select>
                          </div>
                      </div>
                      <div class="mt-4 flex items-center">'''

new_admin_form = '''                          <div>
                              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Subscription Type</label>
                              <select name="subscription_type" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-2">
                                  <option value="Monthly" {% if company and company['subscription_type'] == 'Monthly' %}selected{% endif %}>Monthly</option>
                                  <option value="Annual" {% if company and company['subscription_type'] == 'Annual' %}selected{% endif %}>Annual</option>
                              </select>
                          </div>
                          <div>
                              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Status</label>
                              <select name="status" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-2">
                                  <option value="Active" {% if company and company.get('status') == 'Active' %}selected{% endif %}>Active</option>
                                  <option value="Suspended" {% if company and company.get('status') == 'Suspended' %}selected{% endif %}>Suspended</option>
                              </select>
                          </div>
                          <div>
                              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Portals</label>
                              <select name="portals" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-2">
                                  <option value="Both" {% if company and company.get('portals') == 'Both' %}selected{% endif %}>Both (Forsah & Etimad)</option>
                                  <option value="Forsah" {% if company and company.get('portals') == 'Forsah' %}selected{% endif %}>Forsah Only</option>
                                  <option value="Etimad" {% if company and company.get('portals') == 'Etimad' %}selected{% endif %}>Etimad Only</option>
                              </select>
                          </div>
                          <div>
                              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Expiry Date</label>
                              <input type="date" name="expiry_date" value="{{ company.get('expiry_date', '') if company else '' }}" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-2">
                          </div>
                          <div class="sm:col-span-2">
                              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Report Schedule</label>
                              <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                                  {% set times = company.get('report_times', '09:00,11:00,13:00,15:00').split(',') if company else ['09:00', '11:00', '13:00', '15:00'] %}
                                  <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="09:00" {% if '09:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">09:00 AM</span></label>
                                  <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="11:00" {% if '11:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">11:00 AM</span></label>
                                  <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="13:00" {% if '13:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">01:00 PM</span></label>
                                  <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="15:00" {% if '15:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">03:00 PM</span></label>
                                  <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="17:00" {% if '17:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">05:00 PM</span></label>
                                  <label class="inline-flex items-center"><input type="checkbox" name="report_times" value="19:00" {% if '19:00' in times %}checked{% endif %} class="form-checkbox h-4 w-4 text-blue-600"><span class="ml-2 text-sm text-gray-700 dark:text-gray-300">07:00 PM</span></label>
                              </div>
                          </div>
                      </div>
                      <div class="mt-4 flex items-center">'''

# Let's use a simpler match
code = re.sub(r'(\s*<label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Subscription Type</label>\s*<select name="subscription_type" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-2">\s*<option value="Monthly" {% if company and company\[\'subscription_type\'\] == \'Monthly\' %}selected{% endif %}>Monthly</option>\s*<option value="Annual" {% if company and company\[\'subscription_type\'\] == \'Annual\' %}selected{% endif %}>Annual</option>\s*</select>\s*</div>\s*</div>\s*<div class="mt-4 flex items-center">)', new_admin_form, code, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
