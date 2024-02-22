# 1. expose the local machine to the internet: ssh -R 80:127.0.0.1:5000 serveo.net
# 2. set webhook with the output of previous step
#--- set webhook: 
#       https://api.telegram.org/bot6546517474:AAHBVAesenlhwFL_altk4E-dqwO6xtqh40k/setWebhook?url=https://0e67e13920a0256c617b52a8b15a6eb8.serveo.net
# TODO: having the path to the pages, find a way to save the page as pdf and send it to the telegram user(scrap the page)
# TODO: complete the functinalty of each command and scrap the page 
# TODO: Clean up the code and prepare it to launch on RasperryPi
# TODO: make the ultimate code as a release 
# TODO: make a service on Raspry and run the release code on it
from flask import Flask
from flask import request
from flask import Response
import requests
import json

from scrap_wiki import Scrapper

app = Flask(__name__)

TOKEN = '6546517474:AAHBVAesenlhwFL_altk4E-dqwO6xtqh40k'
txt_welcome = "Welcome to my personal wiki. "
cat_commands_json = ''
cat_dic = [] # command, {catName, address}
wiki_url = "https://api.telegram.org/bot" + TOKEN

def scrapWiki():
    global cat_commands_json
    global wiki_scrapper
    global cat_dic
    wiki_scrapper = Scrapper()
    cat_dic = wiki_scrapper.getCategories()
    
    for key, item in cat_dic.items():
        cat_commands_json += '{"command":"%s", "description":"%s"},'%(key,item[0])
    cat_commands_json = cat_commands_json.rstrip(',')
  
def sendWelcome(chatId, first_name):
    url = wiki_url + "/sendMessage"
    data = {'chat_id': chatId, "text": "%s!\n%s"%(first_name,txt_welcome)}
    r = requests.post(url, data=data)
                
def sendMenu():   
    url = wiki_url + "/setMyCommands"
    # data = {'commands': '[{"command":"h", "description":"Home"},{"command":"a", "description":"aaa"}]'}
    data = {'commands': '[%s]'%cat_commands_json}

    r = requests.post(url, data=data)
    print(r.text)

def sendHome(command):
    print(command)

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
            if raw_json["message"]["text"] == '/h':
                wiki_scrapper.scrapPage('/h'.lstrip('/'))
                sendHome('home page is sending to bot')

        return Response('ok', status=200)
    else:
        return '<h1> My Wiki Bot</h1>'

if __name__ == '__main__':
    scrapWiki()
    app.run(debug=True)