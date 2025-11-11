from flask import Flask, render_template_string
import os

app = Flask(name)

HTML = '''
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head><meta charset="utf-8"><title>شطرنج تتر</title></head>
<body style="background:#111;color:#0f9;font-family:Tahoma;text-align:center;padding:50px">
<h1>شطرنج تتر آنلاین شد! ♟️</h1>
<p>شرط: ۱۰ USDT | برنده: ۱۸ USDT | تقلب = مساوی + ۹ USDT برگشت</p>
<h2>Jamal جان، تو بردی! لینک زنده شد</h2>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

if name == 'main':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
