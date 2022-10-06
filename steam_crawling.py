!pip install selenium
!apt-get update
!apt install chromium-chromedriver

from google.colab import drive
drive.mount('/content/gdriv')

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import csv
import ssl
import re
import datetime
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver',options=options)
url = "https://steamcommunity.com/app/730/reviews/"
driver.get(url)

review_array = []
start = datetime.datetime.now()
end = start + datetime.timedelta(seconds=30)

while True:
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  time.sleep(1.5)
  driver.execute_script("window.scrollBy(0, -1);")
  if datetime.datetime.now() > end:
    break;

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
review_array = []
dummy = "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"
list_ = soup.find_all(class_='apphub_CardTextContent', limit = 100000)

for i in list_:
  review = i.text.strip()
  review = BeautifulSoup(review,"html5lib").get_text()
  review = re.sub(dummy, "", review)
  temp_list = [review]
  review_array.append(temp_list)

with open('review.csv', 'w',newline='') as f: 
    write = csv.writer(f) 
    write.writerows(review_array)