from selenium import webdriver 
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scrapper:  

    def __init__(self) -> None:
        mywiki_website = 'http://10.0.0.69:3000/'

        options = Options()
        # The following two lines should be executed exactly as written; 
        # otherwise, it will not retrieve the correct element since it 
        # will not obtain the maximum window size.
        options.add_argument("--headless=new --window-size=1920x1080")
        options.add_argument('--window-size=1920x1080')

        self.driver = webdriver.Chrome(options=options)

        self.driver.get(mywiki_website)
        # self.driver.maximize_window()
        left_panel_find_element = self.driver.find_element(by='xpath', value="//div[contains(@class,'v-list py-2')]")
        # self.left_panel = driver.find_element(by='xpath', value="//div[contains(@class,'v-list py-2')]")
        left_panel_explicit = WebDriverWait(self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"v-list py-2")]')))
        # self.matches = left_panel.find_elements(by='xpath', value=".//a")
        matches = WebDriverWait(left_panel_explicit, timeout=10).until(EC.presence_of_all_elements_located((By.XPATH, './/a')))
        self.categories = {}
    
        for item in matches:
            self.categories[item.text[0].lower()] = (item.text, item.get_attribute("href"))

        self.driver.quit()
    
    def getCategories(self):
        """
        categpries is a dictionry. 
        key: command, 
        value: (category name, address)
        """
        return self.categories
    
    def scrapPage(self, command):
        url = self.categories[command][1]
        print(url)
        # left_panel_explicit = WebDriverWait(self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"contents")]')))
        # print(left_panel_explicit)
        # self.driver.get(url)
