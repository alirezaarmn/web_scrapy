# 1. expose the local machine to the internet: ssh -R 80:127.0.0.1:5000 serveo.net
# 2. set webhook with the output of previous step
#--- set webhook: 
#       https://api.telegram.org/bot6546517474:AAHBVAesenlhwFL_altk4E-dqwO6xtqh40k/setWebhook?url=https://0e67e13920a0256c617b52a8b15a6eb8.serveo.net
# TODO: Clean up the code and prepare it to launch on RasperryPi
# TODO: make the ultimate code as a release 
# TODO: make a service on Raspry and run the release code on it
from flask import Flask
from flask import request
from flask import Response
import requests
import json

from scrap_wiki import Scrapper
from convert_to_pdf import convert_url_to_pdf

app = Flask(__name__)

TOKEN = '6546517474:AAHBVAesenlhwFL_altk4E-dqwO6xtqh40k'
txt_welcome = "Welcome to my personal wiki. "
cat_commands_json = ''
cat_dic = [] # command, {catName, address}
token_url = "https://api.telegram.org/bot" + TOKEN

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
    url = token_url + "/sendMessage"
    data = {'chat_id': chatId, "text": "%s!\n%s"%(first_name,txt_welcome)}
    r = requests.post(url, data=data)
    print(r.text)
                
def sendMenu():   
    url = token_url + "/setMyCommands"
    # data = {'commands': '[{"command":"h", "description":"Home"},{"command":"a", "description":"aaa"}]'}
    data = {'commands': '[%s]'%cat_commands_json}

    r = requests.post(url, data=data)
    print(r.text)

def sendFile(chatId, doc):
    url = token_url + "/sendDocument?chat_id={}".format(chatId)
    # `files=` should be there. otherwise it does work
    r = requests.post(url, files={'document': open(doc, 'rb')})
    print(r.text)

def sendButton(chatId, buttons):
    url = token_url + "/sendMessage"
    inline_keyboard = ''
    
    # Showing each button in a single row requires new array 
    # into array e.g. use [{}] instead of {} for each button  
    for item in buttons:
        inline_keyboard += '[{"text": "%s", "callback_data": "%s"}],' % (item,item)
    
    inline_keyboard = inline_keyboard.rstrip(',')

    data = {'chat_id': chatId, 'text': "Select a page:", 'parse_mode': 'HTML',
    'reply_markup': '{"inline_keyboard": [%s]}' % (inline_keyboard)}
    r = requests.post(url, data=data)
    print(r.text)

def sendMarkDown(chatId, md_text):
    url = token_url + "/sendMessage"
    data = {'chat_id': chatId, "text": md_text, "parse_mode":"Markdown"}
    r = requests.post(url, data=data)
    print(r.text)

def sendHome(chatId, html_page):
    url = token_url + "/sendMessage"
    data = {'chat_id': chatId, "text": html.escape(html_page), "parse_mode":"HTML"}
    r = requests.post(url, data=data)
    print(r.text)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        raw_json = request.get_json()
        print("---------------------telgram data recieve-----------")
        print(raw_json)
        print("----------end of data-----------------------\n")
        if 'message' in raw_json:
            chat_id = str(raw_json["message"]["chat"]["id"])
            first_name = str(raw_json["message"]["chat"]["first_name"])
            if raw_json["message"]["text"] == '/start':
                sendMenu()
                sendWelcome(chat_id, first_name)
            if raw_json["message"]["text"] == '/h':
                sendMarkDown(chatId=chat_id, md_text="`Preparing PDF version of my resume ...`")
                if convert_url_to_pdf(wiki_scrapper.getCommandAddress('h'), 'home.pdf'):
                    print("PDF generated and saved at google.pdf")
                    sendFile(chatId=chat_id, doc='home.pdf')
                else:
                    print("PDF generation failed") #TODO: send error to user
            if raw_json["message"]["text"] =='/d':
                buttons = wiki_scrapper.scrapContentPage('d')
                sendButton(chatId=chat_id, buttons=buttons)
            if raw_json["message"]["text"] =='/g':
                buttons = wiki_scrapper.scrapContentPage('g')
                sendButton(chatId=chat_id, buttons=buttons)
            if raw_json["message"]["text"] =='/l':
                buttons = wiki_scrapper.scrapContentPage('l')
                sendButton(chatId=chat_id, buttons=buttons)
            if raw_json["message"]["text"] =='/r':
                buttons = wiki_scrapper.scrapContentPage('r')
                sendButton(chatId=chat_id, buttons=buttons)
            if raw_json["message"]["text"] =='/i':
                buttons = wiki_scrapper.scrapContentPage('i')
                sendButton(chatId=chat_id, buttons=buttons)

        elif 'callback_query' in raw_json:
            chat_id = str(raw_json["callback_query"]["from"]["id"])
            pageName = raw_json['callback_query']['data']
            contentAddress = wiki_scrapper.getContentAddress(pageName)
            if convert_url_to_pdf(contentAddress, '{}.pdf'.format(pageName)):
                print("PDF generated and saved at google.pdf")
                sendFile(chatId=chat_id, doc='{}.pdf'.format(pageName))
            else:
                print("PDF generation failed") #TODO: send error to user

        return Response('ok', status=200)
    else:
        return '<h1> My Wiki Bot</h1>'

if __name__ == '__main__':
    scrapWiki()
    app.run(debug=True)