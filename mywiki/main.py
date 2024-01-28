# 1. expose the local machine to the internet: ssh -R 80:127.0.0.1:5000 serveo.net
# 2. set webhook with the output of previous step
#--- set webhook: 
#       https://api.telegram.org/bot6546517474:AAHBVAesenlhwFL_altk4E-dqwO6xtqh40k/setWebhook?url=https://0e67e13920a0256c617b52a8b15a6eb8.serveo.net

# TODO: provide button for the categories

from flask import Flask
from flask import request
from flask import Response
import requests
import json

from scrap_wiki import scrap

app = Flask(__name__)

TOKEN = '6546517474:AAHBVAesenlhwFL_altk4E-dqwO6xtqh40k'
txt_welcome = "خوش آمدید. \n لطفا یکی از مغازه ها رو انتخاب کنید"
btn_saayi = '{"text": "پارک ساعی", "callback_data": "saayi%s" }'
btn_hovize = '{"text": "هویزه", "callback_data": "hovize%s" }'

def write_json(data, filename='response.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def sendWelcome(chatId):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    data = {'chat_id': chatId, 'text': txt_welcome, 'parse_mode': 'HTML',
    'reply_markup': '{"inline_keyboard": [[%s,%s]]}' % (btn_saayi, btn_hovize)}
    r = requests.post(url, data=data)
    print(r.text)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        raw_json = request.get_json()
        print(raw_json)
        if 'message' in raw_json:
            chat_id = str(raw_json["message"]["chat"]["id"])
            if raw_json["message"]["text"] == '/start':
                sendWelcome(chat_id)
        # write_json(msg, 'telgram_logs.json')
        return Response('ok', status=200)
    else:
        sample = scrap()
        print(sample.getCategories())
        return '<h1> My Wiki Bot</h1>'

if __name__ == '__main__':
    app.run(debug=True)