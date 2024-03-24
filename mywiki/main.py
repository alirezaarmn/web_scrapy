# TODO: Clean up the code and prepare it to launch on RasperryPi
# TODO: make the ultimate code as a release 
# TODO: make a service on Raspry and run the release code on it
from flask import Flask
from flask import request
from flask import Response
from scrap_wiki import Scrapper
from tele_bot import TelBot
from logger import Logger
from xhtml2pdf import pisa

import requests
import os

app = Flask(__name__)

tel_bot = TelBot()
logger = Logger("main", "main.log")

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
 
def convert_url_to_pdf(url, file_name): 
    # Fetch the HTML content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        logger.logError(f"Failed to fetch URL: {url}")
        return False
    
    html_content = response.text
    
    # Generate PDF
    with open("{}.pdf".format(file_name), "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        
    return not pisa_status.err

@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        raw_json = request.get_json()
        logger.logDebug(raw_json)
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
                        os.remove('home.pdf')
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
                    doc='{}.pdf'.format(pageName)
                    tel_bot.sendFile(chatId=chat_id, doc=doc)
                    os.remove(doc)
                else:
                    tel_bot.sendError(chat_id, "PDF generation failed")
        except Exception as e:
            logger.logError("Unable to Parse JSON: " + str(e))

        return Response('ok', status=200)
    else:
        return '<h1> My Wiki Bot</h1>'

if __name__ == '__main__':
    scrapWiki()
    app.run(debug=True)