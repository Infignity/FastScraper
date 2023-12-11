'''scrapper modules'''
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By


class ScrapperHelper:
    '''Web Scrappers Helpers'''

    @staticmethod
    def bs4(contents):
        '''applying beautiful soup'''
        soup = BeautifulSoup(contents, "html.parser")
        return soup.get_text()

    @staticmethod
    def selen(url):
        '''using selenium'''
        options = Options()
        options.headless = True  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.binary_location = os.environ.get("GOOGLE_CHROME_SHIM")

        # Initialize the WebDriver
        driver = webdriver.Chrome(options=options)

        try:
            # Navigate to the company website
            driver.get(url)
            time.sleep(5)

            # Scrape the necessary data
            element = driver.find_element(By.TAG_NAME, 'html')
            
            # Retrieve all text from the element
            all_text = element.text

            return all_text

        except WebDriverException as e:
            print(f"An error occurred while trying to scrape {url}: {e}")
            return None
        finally:
            # Close the WebDriver
            driver.quit()
 
 