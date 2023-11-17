from flask import Flask, render_template
app = Flask(__name__)
from bs4 import BeautifulSoup
import requests

# ------------------------------------------- sample 1 --------------------

# source=requests.get('http://quotes.toscrape.com').text
# soup=BeautifulSoup(source, 'lxml')

# quote=soup.find('div', class_='quote')
# quotetext=quote.span.text
# print(quote)

# author=soup.find('small', class_='author')
# authortext=author.text
# print(authortext)

# @app.route('/')
# def home():
#     return render_template('home.html', quotetext=quotetext, authortext=authortext)

# ------------------------------------------- sample 2 --------------------

# url = "https://www.worldometers.info/coronavirus/" #this initiates an HTTP request to get the HTML doc in response
# req = requests. get (url)
# bsobj = BeautifulSoup (req. text, "html.parser") #we create the BeautifulSoup object
# #giving it the HTML response text and specifying the parser as html.parser
# #div tag with class maincounter-number. There are three div tags with this class.
# data = bsobj.find_all("div", class_ = "maincounter-number")

# totalcases=data[0].text.strip() #finding the first element - that is 0 of the three 
# recovered=data[2].text.strip() #finding element three - that is index 02 of the three

# totalcases= int(data[0].text.strip().replace(',','')) #here we get rid of the comma and cast to integer
# recovered = int(data[2].text.strip().replace(',',''))

# percentagerecovered=recovered/totalcases*100 #so that we can do some cool calculations 
# percentagerecovered=round(percentagerecovered,2)

# @app.route('/')
# def home(): #do not forget to pass in the variables to the home.html page
#     return render_template('home.html',totalcases=totalcases,recovered=recovered,percentagerecovered=percentagerecovered)

# ------------------------------------------- sample 3 --------------------

url = 'https://en.m.wikipedia.org/wiki/List_of_largest_Internet_companies'
req = requests.get(url)
bsObj = BeautifulSoup(req.text, 'html.parser')
data = bsObj.find('table',{'class': 'wikitable sortable mw-collapsible'})

table_data=[]
trs = bsObj.select('table tr')
for tr in trs[1:6]: #first element is empty
    row = []
    for t in tr.select('td')[:3]:
        row. extend([t.text.strip()])
    table_data. append (row)
data=table_data
#td is referring to the columns

@app.route('/')
def home(): #do not forget to pass in the variables to the home.html page
    return render_template('home.html',data=data)

if __name__ == '__name__':
    app.run(debug=True)