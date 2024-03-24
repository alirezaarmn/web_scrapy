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
        # left_panel_find_element = self.driver.find_element(by='xpath', value="//div[contains(@class,'v-list py-2')]")
        # self.left_panel = driver.find_element(by='xpath', value="//div[contains(@class,'v-list py-2')]")
        left_panel_explicit = WebDriverWait(self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"v-list py-2")]')))
        # self.matches = left_panel.find_elements(by='xpath', value=".//a")
        matches = WebDriverWait(left_panel_explicit, timeout=10).until(EC.presence_of_all_elements_located((By.XPATH, './/a')))
        self.categories = {}
        self.contentPage = {}
    
        for item in matches:
            self.categories[item.text[0].lower()] = (item.text, item.get_attribute("href"))

    def __del__(self) -> None:
        self.driver.quit()
    
    def getCategories(self):
        """
        categpries is a dictionry. 
        key: command, 
        value: (category name, address)
        """
        return self.categories
    
    def scrapContentPage(self, chatId, command):
        """
        Retrieve the corresponding page of the command and scrape the page.
        """
        self.contentPage[chatId] = {}

        if command not in self.categories:
            return self.contentPage[chatId]

        url = self.categories[command][1]
        self.driver.get(url)
        matches = WebDriverWait(self.driver, timeout=10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"contents")]//ul//li//a')))

        for item in matches:
            self.contentPage[chatId][item.text] = item.get_attribute("href")

        return self.contentPage[chatId].keys()

    def getCommandAddress(self, command):
        """
        Retrieve the address of command
        """
        if command not in self.categories:
            return {}
        
        return self.categories[command][1]
    
    def getContentAddress(self, chatId, contentTitle):
        """
        """
        if contentTitle in self.contentPage[chatId]:
            return self.contentPage[chatId][contentTitle]
        else:
            print("Page not found.")
            return ''
