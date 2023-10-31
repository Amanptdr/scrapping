from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from time import sleep
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from translate import Translator
from googletrans import Translator
import requests
translator = Translator()


link = 'http://vpcqcsdt.bocongan.gov.vn/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3/ctl/chitiet/mid/1088/ma/d8240214-eef2-4c58-8202-99387fe818cd?returnUrl=/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3'
res = requests.get(link)
soup = BeautifulSoup(res.text,'html.parser')
table = soup.find("table")
table_data = []
table_headers = []
for row in table.find_all('tr'):
  for th in row.find_all('th'):
    text_to_translate = th.text.strip()
    try:
      translated_text = translator.translate(text_to_translate, src='vi', dest='en')
      table_headers.append(translated_text.text)
    except:
      table_headers.append(text_to_translate)
for row in table.find_all('tr'):
  total = len(row.find_all('th'))
  for td in row.find_all('td'):
    if total>0:
      if 'noborder' in td.get('class', []):
        total = total-1
        continue
      text_to_translate = td.text.strip()
      try:
        translated_text = translator.translate(text_to_translate, src='vi', dest='en')
        table_data.append(translated_text.text)
      except:
          table_data.append(text_to_translate)
      total = total-1

print(table_headers)
print(table_data)
df = pd.DataFrame([table_data], columns=table_headers)
df.to_excel("web_scraped_data1111.xlsx", index=False)




# for row in table.find_all('tr'):
#   for td in row.find_all('td'):
#       if 'noborder' in td.get('class', []):
#         continue
#       text_to_translate = td.text.strip()
#       try:
#         translated_text = translator.translate(text_to_translate, src='vi', dest='en')
#         table_data.append(translated_text.text)
#       except:
#           table_data.append(text_to_translate)