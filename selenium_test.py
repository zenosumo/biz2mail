from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Path to the ChromeDriver executable
CHROMEDRIVER_PATH = '/path/to/chromedriver'  # Update this path

def check_selenium_setup():
    options = Options()
    options.add_argument("--headless")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://duckduckgo.com/")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("2100890967 SIS TER")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Allow time for the results to load

        results = driver.find_elements(By.CLASS_NAME, 'result__a')
        if results:
            print("Selenium is set up correctly.")
            print("First result URL:", results[0].get_attribute('href'))
        else:
            print("No results found. Please check the setup.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_selenium_setup()
