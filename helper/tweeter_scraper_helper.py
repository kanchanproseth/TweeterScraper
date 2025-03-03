import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helper.string_converter_helper import *
from helper.resource_path_helper import *
import os

def get_twitter_metrics(tweet_url):
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")  # Disables the 'Chrome is being controlled by automated test software' infobar
    chrome_options.add_argument("--disable-extensions")  # Disables extensions
    chrome_options.add_argument("--headless")  # Remove headless to debug
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chromedriver_path = resource_path(os.path.join("drivers", "chromedriver.exe"))
    service = Service(chromedriver_path)  # Ensure correct ChromeDriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(tweet_url)

        wait = WebDriverWait(driver, 20)  # Wait up to 10 sec for elements

        like_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='like']")))
        retweet_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='retweet']")))
        like_value = ''
        retweet_value = ''
        
        like_value = '0' if not like_button.text else convert_suffixed_value(like_button.text)
        retweet_value = '0' if not retweet_button.text else convert_suffixed_value(retweet_button.text)
        return {"like": like_value, "retweet": retweet_value}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

    finally:
        driver.quit()

# tweet_url = "https://twitter.com/ClutchPoints/status/1895706965210439978"  # Replace with any valid tweet URL
# result = get_twitter_metrics(tweet_url)
# print(result) 