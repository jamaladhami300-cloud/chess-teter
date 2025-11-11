from flask import Flask, render_template_string, request, jsonify
from tronapi import Tron
import os
from dotenv import load_dotenv
import chess
import time

load_dotenv()
app = Flask(name)

tron = Tron()
tron.private_key = os.getenv('TEMP_PRIVATE_KEY')
tron.default_address = os.getenv('TEMP_WALLET')

COMMISSION_WALLET = os.getenv('COMMISSION_WALLET')
TEMP_WALLET = os.getenv('TEMP_WALLET')

games = {}

HTML = '''
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head><meta charset="utf-8"><title>شطرنج تتر</title></head>
<body style="background:#111;color:#0f9;font-family:Tahoma;text-align:center;padding:50px">
<h1>شطرنج تتر آنلاین شد! ♟️</h1>
<p>شرط: ۱۰ USDT | برنده: ۱۸ USDT | کارمزد: ۲ USDT (مال جمال)</p>
<p>مساوی/پات/تقلب = ۹ USDT به هر دو</p>
<h2>Jamal جان، هر بازی ۲ تتر سود خالص!</h2>
<p>لینک: <a href="https://chess-teter.netlify.app" style="color:#0ff">chess-teter.netlify.app</a></p>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/start', methods=['POST'])
def start():
    wallet = request.json['wallet']
    room = str(time.time())[-8:]
    games[room] = {'p1': wallet, 'board': chess.Board(), 'paid': False}
    return jsonify({'room': room, 'temp_wallet': TEMP_WALLET, 'amount': 10})

@app.route('/join', methods=['POST'])
def join():
    data = request.json
    room = data['room']
    wallet = data['wallet']
    if room in games and 'p2' not in games[room]:
        games[room]['p2'] = wallet
        games[room]['paid'] = True
        return jsonify({'status': 'ready'})
    return jsonify({'error': 'full'}), 400

@app.route('/result', methods=['POST'])
def result():
    data = request.json
    room = data['room']
    outcome = data['outcome']  # "win_white", "win_black", "draw", "cheat"
    
    if room not in games or not games[room]['paid']:
        return jsonify({'error': 'not paid'}), 400
    
    p1 = games[room]['p1']
    p2 = games[room]['p2']
    
    # ۲ تتر کارمزد همیشه مال تو
    send_usdt(COMMISSION_WALLET, 2)
    
    if outcome == "win_white":
        send_usdt(p1, 18)
    elif outcome == "win_black":
        send_usdt(p2, 18)
    else:  # draw, stalemate, cheat
        send_usdt(p1, 9)
        send_usdt(p2, 9)
    
    del games[room]
    return jsonify({'status': 'paid'})

def send_usdt(to, amount):
    try:
        contract = tron.trx.get_contract('TR7NHqjeKQxGTCuuP8qACi6iF2iGLCzvM')  # USDT
        tx = contract.functions.transfer(to, amount * 1000000).build()
        tx = tx.sign(tron.private_key).broadcast()
    except:
        pass

if name == 'main':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
