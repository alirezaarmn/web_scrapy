from selenium import webdriver
import time

website = 'https://www.audible.ca/ep/audiobooks?ref_pageloadid=not_applicable&ref=a_hp_t1_navTop_pl0cg0c0r0&pf_rd_p=36c4a793-abb3-47c2-a362-79f8f7efd7ab&pf_rd_r=C06P2MY167WGJHKS8XEN&pageLoadId=3Iikzpp2bv1InNQQ&ref_plink=not_applicable&creativeId=5cf63ff8-590d-4664-a9e1-e552dde3902f'

driver = webdriver.Chrome()

driver.get(website)
driver.maximize_window()

elements = driver.find_elements(by='xpath', value='//div[@data-trigger="product-list-flyout-B0BNLNPG7D"]')
slicks = driver.find_elements(by='xpath', value='//div[@class="adbl-impression-container "]')
trending = driver.find_elements(by='xpath', value="//div[@id='adbl-web-carousel-c5']//div[contains(@class,'carousel-product')]")

books = []

for match in trending:
    book_name = match.find_element(by='xpath', value='.//span[contains(@class,"bc-text")]').text
    # time.sleep(5)
    if book_name == '':
        next_button = match.find_element(by='xpath', value='//i[@id="slidemove-right-c5"]')
        next_button.click()
        time.sleep(5)
        book_name = match.find_element(by='xpath', value='.//span[contains(@class,"bc-text")]').text
        
    print(book_name)
    books.append(book_name)
print(len(books))
driver.quit()