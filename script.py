import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

en_btn = '''<button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                              Subscribe Now & Start Trial
                          </button>'''

new_en_btn = '''<div class="mb-6">
                              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Preferred Report Times (Hold Ctrl/Cmd for multiple)</label>
                              <select name="report_times" multiple class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-3 bg-gray-50 dark:bg-gray-700 dark:text-white h-32">
                                  <option value="09:00" selected>09:00 AM</option>
                                  <option value="11:00" selected>11:00 AM</option>
                                  <option value="13:00" selected>01:00 PM</option>
                                  <option value="15:00" selected>03:00 PM</option>
                                  <option value="17:00">05:00 PM</option>
                                  <option value="19:00">07:00 PM</option>
                              </select>
                          </div>
                          <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                              Subscribe Now & Start Trial
                          </button>'''
code = code.replace(en_btn, new_en_btn)

ar_btn = '''<button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                              اشترك الآن وابدأ الفترة التجريبية
                          </button>'''

new_ar_btn = '''<div class="mb-6">
                              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">أوقات استلام التقرير المفضلة (اضغط Ctrl/Cmd لاختيار أكثر من وقت)</label>
                              <select name="report_times" multiple class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border p-3 bg-gray-50 dark:bg-gray-700 dark:text-white h-32">
                                  <option value="09:00" selected>09:00 صباحاً</option>
                                  <option value="11:00" selected>11:00 صباحاً</option>
                                  <option value="13:00" selected>01:00 مساءً</option>
                                  <option value="15:00" selected>03:00 مساءً</option>
                                  <option value="17:00">05:00 مساءً</option>
                                  <option value="19:00">07:00 مساءً</option>
                              </select>
                          </div>
                          <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                              اشترك الآن وابدأ الفترة التجريبية
                          </button>'''
code = code.replace(ar_btn, new_ar_btn)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
