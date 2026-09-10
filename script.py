with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("<div>                          <div>\n                              <label class=\"block text-sm font-medium text-gray-700 dark:text-gray-300\">Subscription Type</label>", "                          <div>\n                              <label class=\"block text-sm font-medium text-gray-700 dark:text-gray-300\">Subscription Type</label>")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
