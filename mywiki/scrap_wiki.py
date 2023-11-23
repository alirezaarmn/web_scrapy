from selenium import webdriver 
from selenium.webdriver.remote.webelement import WebElement

mywiki_website = 'http://10.0.0.69:3000/'

driver = webdriver.Chrome()

driver.get(mywiki_website)
driver.maximize_window()

left_panel = driver.find_element(by='xpath', value="//div[contains(@class,'v-list py-2')]")
matches = left_panel.find_elements(by='xpath', value=".//a")
categories = {}#key:name, value:link

for item in matches:
    categories[item.text] = item.get_attribute("href")

print(categories)
driver.quit()