import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

def replace_nth(string, old, new, n):
    parts = string.split(old, n+1)
    if len(parts) <= n+1:
        return string
    return old.join(parts[:-1]) + new + parts[-1]

old_str = '''                    </div>
                    <div class="pt-4">
                        <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-lg font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150">
                            Start 7-Day Free Trial
                        </button>'''

new_en = '''                    </div>
                    <div class="mb-6">
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
                    <div class="pt-4">
                        <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-lg font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150">
                            Start 7-Day Free Trial
                        </button>'''

code = code.replace(old_str, new_en)

old_ar = '''                    </div>
                    <div class="pt-4">
                        <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-lg font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150">
                            ابدأ تجربتك المجانية لمدة 7 أيام
                        </button>'''

new_ar = '''                    </div>
                    <div class="mb-6">
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
                    <div class="pt-4">
                        <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-lg font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150">
                            ابدأ تجربتك المجانية لمدة 7 أيام
                        </button>'''

code = code.replace(old_ar, new_ar)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
