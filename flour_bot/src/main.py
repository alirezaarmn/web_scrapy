#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import time
import json
import ssl
# import telepot
from http.server import BaseHTTPRequestHandler, HTTPServer
import traceback
import sys


TOKEN = '850453809:AAHBFd6TUMjZsWCpSAC4FzfUcW0EdDnycSs'
HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8443
SAAYI = ('bu1-23815', '1gL463')
HOVIZE = ('bu1-23803', '5kR3E9')

data = {}
headers = {
    'Origin': 'https://eflour.ir',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.94 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://eflour.ir/login.aspx?RA=1&PR=0&ReturnUrl='
               'http%3a%2f%2feflour.ir%2fPages%2fReport%2fDashBoard.aspx',
    'Connection': 'keep-alive',
    'DNT': '1',
}

params = (
    ('RA', '1'),
    ('PR', '0'),
    ('ReturnUrl', 'http://eflour.ir/Pages/Report/DashBoard.aspx'),
)

session = requests.sessions.session()
# TelegramBot = telepot.Bot(TOKEN)


def log_in(chat_id, store):
    r = session.get("https://eflour.ir/login.aspx")
    soup = BeautifulSoup(r.text, features="lxml")
    img = soup.find('div', attrs={"class": "form-item captcha"}).find('img')
    inputs = soup.find("form", attrs={'id': 'form1'}).find_all('input')

    for i in inputs:
        data[i['name']] = i['value'] if 'value' in i.attrs else ''

    data['ctl00$MainContentPlaceHolder$txtUsername'] = store[0]
    data['ctl00$MainContentPlaceHolder$txtPassword'] = store[1]

    # TelegramBot.sendPhoto(chat_id, "https://eflour.ir/" + img['src'])
    sendPhoto(chat_id, "https://eflour.ir/" + img['src'])


def scrap_content(chat_id, r):
    try:
        soup = BeautifulSoup(r, features="lxml")
        table = soup.find('table',attrs={"class":"form"})
        rows = {}
        msg = ""
        if table:
            rows = table.findAll('tr')
        else:
            print("wrong captch")
            sendError(chat_id)

        for row in rows:
            if row.text.find("سقف خرید ماهانه (کیلوگرم):") == 1:
                a = int((int(row.findAll('span')[0].text))/40)
                b = int((int(row.findAll('span')[1].text))/40)
                msg = "سقف خرید ماهیانه(کیسه):" + str(a) + "\n"+ "خرید این ماه(کیسه):" + str(b)
            elif row.text.find("باقیمانده (کیلوگرم):") == 1:
                a = int((int(row.find('span').text)/40))
                msg += "\n" + "باقیمانده این ماه(کیسه):" + str(a)

        if msg != "":
            # TelegramBot.sendMessage(chat_id, msg)
            sendMsg(chat_id, msg)

    except Exception as e:
        print("Unable to Parse JSON" + e)


txt_welcome = "خوش آمدید. \n لطفا یکی از مغازه ها رو انتخاب کنید"
btn_saayi = '{"text": "پارک ساعی", "callback_data": "saayi%s" }'
btn_hovize = '{"text": "هویزه", "callback_data": "hovize%s" }'


def sendWelcome(chatId):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    data = {'chat_id': chatId, 'text': txt_welcome, 'parse_mode': 'HTML',
    'reply_markup': '{"inline_keyboard": [[%s,%s]]}' % (btn_saayi, btn_hovize)}
    r = requests.post(url, data=data)
    print(r.text)

def sendError(chatId):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    data = {'chat_id': chatId, 'text': 'کپچا اشتباه است دوباره امتحان کنید.'}
    r = requests.post(url, data=data)
    print(r.text)

# def send_welcome(chat_id):
    # TelegramBot.sendMessage(chat_id, txt_welcome, 'HTML',
    #                         None,
    #                         None,
    #                         None,
    #                         '{"inline_keyboard": [[%s,%s]]}' % (btn_saayi, btn_hovize))


def sendMsg(chatId, text):
    url = "https://api.telegram.org/bot"+TOKEN+"/sendMessage"
    data = {'chat_id': chatId, 'text': text, 'parse_mode': 'HTML'}
    r = requests.post(url, data=data)


def sendPhoto(chatId, photo):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendPhoto"
    data = {'chat_id': chatId, 'photo': photo, 'parse_mode': 'HTML'}
    r = requests.post(url, data=data)

class MyHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        update = json.loads(self.data_string.decode())
        print(update)

        try:
            if 'message' in update:
                chat_id = str(update["message"]["chat"]["id"])
                if update["message"]["text"] == '/start':
                    # TelegramBot.sendMessage(chat_id, "خوش آمدید")
                    sendWelcome(chat_id)
                elif update["message"]["text"] == '/hov':
                    log_in(chat_id, HOVIZE)
                elif update["message"]["text"] == '/saa':
                    log_in(chat_id, SAAYI)
                else:
                    print(update["message"]["text"])
                    data['ctl00$MainContentPlaceHolder$Captcha1'] = update["message"]["text"]
                    session.post('https://eflour.ir/login.aspx', headers=headers, params=params, data=data)
                    response = session.post('https://eflour.ir/pages/buy/orderrequeststep1.aspx', headers=headers,
                                            params=params, data=data)
                    scrap_content(chat_id, response.text)

        except Exception as e:
            print("Unable to Parse JSON" + str(e))
            sys.stderr.write(traceback.format_exc())

        try:
            if 'callback_query' in update:
                chat_id = str(update["callback_query"]["from"]["id"])
                if 'saayi' in update['callback_query']['data']:
                    log_in(chat_id, SAAYI)
                elif 'hovize' in update['callback_query']['data']:
                    log_in(chat_id, HOVIZE)
        except Exception as e:
            print("Unable to Parse JSON" + e)

        self.respond({'status': 200})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
        <html><head><title>Title goes here.</title></head>
        <body><p>This is a test.</p>
        <p>You accessed path: {}</p>
        </body></html>
        '''.format(path)
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)


httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
# httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
#                                        certfile="/etc/letsencrypt/live/idealhome.ir/fullchain.pem",
#                                        keyfile="/etc/letsencrypt/live/idealhome.ir/privkey.pem")

print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
