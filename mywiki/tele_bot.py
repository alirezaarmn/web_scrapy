from logger import Logger
import requests

class TelBot:
    
    def __init__(self) -> None:
        my_token = '6546517474:AAHBVAesenlhwFL_altk4E-dqwO6xtqh40k'
        self.txt_welcome = "Welcome to my personal wiki. "
        self.token_url = "https://api.telegram.org/bot" + my_token
        self.logger = Logger("telbot.log")

    def sendWelcome(self, chatId, first_name):
        url = self.token_url + "/sendMessage"
        data = {'chat_id': chatId, "text": "%s!\n%s"%(first_name,self.txt_welcome)}
        r = requests.post(url, data=data)
        self.logger.logDebug(r.text)
                
    def sendMenu(self, menu):   
        url = self.token_url + "/setMyCommands"
        # data = {'commands': '[{"command":"h", "description":"Home"},{"command":"a", "description":"aaa"}]'}
        data = {'commands': '[%s]'%menu}

        r = requests.post(url, data=data)
        self.logger.logDebug(r.text)

    def sendFile(self, chatId, doc):
        url = self.token_url + "/sendDocument?chat_id={}".format(chatId)
        # `files=` should be there. otherwise it does work
        r = requests.post(url, files={'document': open(doc, 'rb')})
        self.logger.logDebug(r.text)

    def sendButton(self, chatId, buttons):
        url = self.token_url + "/sendMessage"
        inline_keyboard = ''
        
        # Showing each button in a single row requires new array 
        # into array e.g. use [{}] instead of {} for each button  
        for item in buttons:
            inline_keyboard += '[{"text": "%s", "callback_data": "%s"}],' % (item,item)
        
        inline_keyboard = inline_keyboard.rstrip(',')

        data = {'chat_id': chatId, 'text': "Select a page:", 'parse_mode': 'HTML',
        'reply_markup': '{"inline_keyboard": [%s]}' % (inline_keyboard)}
        r = requests.post(url, data=data)
        self.logger.logDebug(r.text)

    def sendMarkDown(self, chatId, md_text):
        url = self.token_url + "/sendMessage"
        data = {'chat_id': chatId, "text": md_text, "parse_mode":"Markdown"}
        r = requests.post(url, data=data)
        self.logger.logDebug(r.text)

    def sendHome(self, chatId, html_page):
        url = self.token_url + "/sendMessage"
        data = {'chat_id': chatId, "text": html.escape(html_page), "parse_mode":"HTML"}
        r = requests.post(url, data=data)
        self.logger.logDebug(r.text)

    def sendError(self, chatId, error_text):
        url = self.token_url + "/sendMessage"
        data = {'chat_id': chatId, "text": "<b>{}</b>".format(error_text), "parse_mode":"HTML"}
        r = requests.post(url, data=data)
        self.logger.logDebug(r.text)