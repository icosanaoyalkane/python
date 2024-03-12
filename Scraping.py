import urllib.request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def scraping(url,keyword):
    # ヘッドレスモードでChromeを起動
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
    
    #ChromeでURLにアクセスした先のHTMLを取得
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    #キーワード判定
    if keyword in soup.text:
        print("キーワードが見つかりました。")
        result = 1
    
    else:
        print("キーワードが見つかりませんでした。")
        result = 0

    print('result: '+ str(result))
    print('\n---------\n')
    return result

    driver.quit()

