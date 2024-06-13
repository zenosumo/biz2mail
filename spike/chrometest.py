from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Assuming you've placed chromedriver in your PATH
service = Service('/home/kris/bin/chromedriver')  # Use this if not in your PATH
driver = webdriver.Chrome(service=service)

driver.get("https://www.google.com/") 
