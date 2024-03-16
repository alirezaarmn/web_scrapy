# TODO: Clean up the code and prepare it to launch on RasperryPi
# TODO: make the ultimate code as a release 
# TODO: make a service on Raspry and run the release code on it
from flask import Flask
from flask import request
from flask import Response

from scrap_wiki import Scrapper
from convert_to_pdf import convert_url_to_pdf
from tele_bot import TelBot
from logger import Logger, LogLevel

app = Flask(__name__)

tel_bot = TelBot()
logger = Logger()

def scrapWiki():
    global menu_list
    global wiki_scrapper
    cat_dic = [] # command, {catName, address}
    menu_list = ''
    wiki_scrapper = Scrapper()
    cat_dic = wiki_scrapper.getCategories()
    
    for key, item in cat_dic.items():
        menu_list += '{"command":"%s", "description":"%s"},'%(key,item[0])
    menu_list = menu_list.rstrip(',')
 
@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        raw_json = request.get_json()
        # logger.log(LogLevel.DEBUG, 202, raw_json)
        try:
            if 'message' in raw_json:
                chat_id = str(raw_json["message"]["chat"]["id"])
                first_name = str(raw_json["message"]["chat"]["first_name"])
                if raw_json["message"]["text"] == '/start':
                    tel_bot.sendMenu(menu_list)
                    tel_bot.sendWelcome(chat_id, first_name)
                elif raw_json["message"]["text"] == '/h':
                    tel_bot.sendMarkDown(chatId=chat_id, md_text="`Preparing PDF version of my resume ...`")
                    if convert_url_to_pdf(wiki_scrapper.getCommandAddress('h'), 'home'):
                        tel_bot.sendFile(chatId=chat_id, doc='home.pdf')
                    else:
                        tel_bot.sendError(chat_id, "PDF generation failed")
                else:
                    command = raw_json["message"]["text"]
                    command = command.strip('/')
                    buttons = wiki_scrapper.scrapContentPage(command)
                    if not buttons:
                        tel_bot.sendError(chat_id, "Invalid command")
                    else: 
                        tel_bot.sendButton(chatId=chat_id, buttons=buttons)
            elif 'callback_query' in raw_json:
                chat_id = str(raw_json["callback_query"]["from"]["id"])
                pageName = raw_json['callback_query']['data']
                contentAddress = wiki_scrapper.getContentAddress(pageName)
                if contentAddress == '':
                    tel_bot.sendError(chat_id, "Invalid page request, please first send a valid command")
                if convert_url_to_pdf(contentAddress, pageName):
                    tel_bot.sendFile(chatId=chat_id, doc='{}.pdf'.format(pageName))
                else:
                    tel_bot.sendError(chat_id, "PDF generation failed")
        except Exception as e:
            print("Unable to Parse JSON: " + str(e))

        return Response('ok', status=200)
    else:
        return '<h1> My Wiki Bot</h1>'

if __name__ == '__main__':
    scrapWiki()
    app.run(debug=True)