# 1. expose the local machine to the internet: ssh -R 80:127.0.0.1:5000 serveo.net
# 2. set webhook with the output of previous step
#--- set webhook: 
#       https://api.telegram.org/bot6546517474:AAHBVAesenlhwFL_altk4E-dqwO6xtqh40k/setWebhook?url=https://0e67e13920a0256c617b52a8b15a6eb8.serveo.net

# TODO: scraping should be perform once and at the startup, not in the /start command

from flask import Flask
from flask import request
from flask import Response
import requests
import json

from scrap_wiki import scrap

app = Flask(__name__)

TOKEN = '6546517474:AAHBVAesenlhwFL_altk4E-dqwO6xtqh40k'
txt_welcome = "Welcome to my personal wiki. "

def write_json(data, filename='response.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def sendWelcome(chatId, first_name):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    data = {'chat_id': chatId, "text": "%s!\n%s"%(first_name,txt_welcome)}
    r = requests.post(url, data=data)

def sendMenu():
    sample = scrap()
    temp = sample.getCategories()
    print(sample.getCategories())

    cat = ''
    for item in temp:
        cat += '{"command":"%s", "description":"%s"},'%(item[0].lower(),item)
    cat = cat[:-1] #TODO: is there any better solution for removing the , at the end of string?
    print(cat)
    url = "https://api.telegram.org/bot" + TOKEN + "/setMyCommands"
    # data = {'commands': '[{"command":"h", "description":"Home"},{"command":"a", "description":"aaa"}]'}
    data = {'commands': '[%s]'%cat}

    r = requests.post(url, data=data)
    print(r.text)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        raw_json = request.get_json()
        print(raw_json)
        if 'message' in raw_json:
            chat_id = str(raw_json["message"]["chat"]["id"])
            first_name = str(raw_json["message"]["chat"]["first_name"])
            if raw_json["message"]["text"] == '/start':
                sendMenu()
                sendWelcome(chat_id, first_name)
        # write_json(msg, 'telgram_logs.json')
        return Response('ok', status=200)
    else:
        return '<h1> My Wiki Bot</h1>'

if __name__ == '__main__':
    app.run(debug=True)