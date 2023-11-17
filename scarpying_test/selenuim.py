from selenium import webdriver

website = 'https://www.salomon.com/en-ca/shop/checkout/onepage/success/'
path = '/usr/bin/safaridriver'
# driver = webdriver.Safari(path)

driver = webdriver.Safari(executable_path='/System/Cryptexes/App/usr/bin/safaridriver')
# or
# driver = webdriver.Safari()
driver.get(website)

# driver.quit()