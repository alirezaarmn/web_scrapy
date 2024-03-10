# TODO: Clean up the code and prepare it to launch on RasperryPi
# TODO: make the ultimate code as a release 
# TODO: make a service on Raspry and run the release code on it
from flask import Flask
from flask import request
from flask import Response

from scrap_wiki import Scrapper
from convert_to_pdf import convert_url_to_pdf
from tele_bot import TelBot

app = Flask(__name__)

tel_bot = TelBot()

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
        print("---------------------telgram data recieve-----------")
        print(raw_json)
        print("----------end of data-----------------------\n")
        if 'message' in raw_json:
            chat_id = str(raw_json["message"]["chat"]["id"])
            first_name = str(raw_json["message"]["chat"]["first_name"])
            if raw_json["message"]["text"] == '/start':
                tel_bot.sendMenu(menu_list)
                tel_bot.sendWelcome(chat_id, first_name)
            elif raw_json["message"]["text"] == '/h':
                tel_bot.sendMarkDown(chatId=chat_id, md_text="`Preparing PDF version of my resume ...`")
                if convert_url_to_pdf(wiki_scrapper.getCommandAddress('h'), 'home'):
                    print("PDF generated and saved at google.pdf")
                    tel_bot.sendFile(chatId=chat_id, doc='home.pdf')
                else:
                    print("PDF generation failed") #TODO: send error to user
            else:
               command = raw_json["message"]["text"]
               command = command.strip('/')
               buttons = wiki_scrapper.scrapContentPage(command)
               tel_bot.sendButton(chatId=chat_id, buttons=buttons)

        elif 'callback_query' in raw_json:
            chat_id = str(raw_json["callback_query"]["from"]["id"])
            pageName = raw_json['callback_query']['data']
            contentAddress = wiki_scrapper.getContentAddress(pageName)
            if convert_url_to_pdf(contentAddress, pageName):
                print("PDF generated and saved at google.pdf")
                tel_bot.sendFile(chatId=chat_id, doc='{}.pdf'.format(pageName))
            else:
                print("PDF generation failed") #TODO: send error to user

        return Response('ok', status=200)
    else:
        return '<h1> My Wiki Bot</h1>'

if __name__ == '__main__':
    scrapWiki()
    app.run(debug=True)