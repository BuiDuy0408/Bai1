from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://google.com')
print(driver.page_source)