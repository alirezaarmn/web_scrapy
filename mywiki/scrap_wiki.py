from selenium import webdriver 
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class scrap:  

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
        self.left_panel_find_element = self.driver.find_element(by='xpath', value="//div[contains(@class,'v-list py-2')]")
        # self.left_panel = driver.find_element(by='xpath', value="//div[contains(@class,'v-list py-2')]")
        self.left_panel_explicit = WebDriverWait(self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"v-list py-2")]')))
        # self.matches = left_panel.find_elements(by='xpath', value=".//a")
        self.matches = WebDriverWait(self.left_panel_explicit, timeout=10).until(EC.presence_of_all_elements_located((By.XPATH, './/a')))
        self.categories = {}
    
        for item in self.matches:
            self.categories[item.text] = item.get_attribute("href")

        self.driver.quit()
    
    def getCategories(self):
        return self.categories
