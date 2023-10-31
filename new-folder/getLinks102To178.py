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
# Configure the web driver (change to your preferred browser)
url = "http://vpcqcsdt.bocongan.gov.vn/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3"
# Navigate to the website with pagination
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 1)
table = driver.find_element(By.XPATH, "//table")
pagination = driver.find_element(By.XPATH,'//*[@id="dnn_ctr1088_ModuleContent"]/table/tbody/tr')
soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
page = BeautifulSoup(pagination.get_attribute('outerHTML'), "html.parser")
table_headers = []
table_data = []
def getPageData():
    table = driver.find_element(By.XPATH, '//table')
    soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
    print("start Second Step ----------222222222222222222222222222222222222222222")
    try:
      for row in soup.find_all('tr'):
        second_td = row.find_all('td')
        for td in second_td:
          link_element = td.find('a')
          if link_element:
            link = link_element.get('href')
            table_data.append(link)
            print("Link:LinkLinkLinkLinkLinkLinkLinkLink", link)
            break
          else:
            print("No link found in the second <td>.")
    except Exception as e:
        print(f"Error waiting for element: {e}")

pageNo = 0
while True:
    print("start first Step ----------1111111111111111111111111111111111111111111111111111")
    page_table = driver.find_element(By.XPATH, '//*[@id="dnn_ctr1088_ModuleContent"]/table')
    page_rows = page_table.find_elements(By.TAG_NAME, 'tr')
    for row in page_rows:
      if pageNo == 0:
        last_td = row.find_elements(By.TAG_NAME, 'td')[-1]
      else:
        last_td = row.find_elements(By.TAG_NAME, 'td')[2]
      last_td_xpath = driver.execute_script("return arguments[0].getAttribute('xpath')", last_td)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, str(last_td_xpath))))
    except Exception as e:
        print(f"Error waiting for element: {e}")
    if last_td.is_enabled() and pageNo<77:
        last_td.click()
        print(pageNo,'111111111111111111111111111111111111111111111111111111111111111')
        getPageData()
        pageNo+=1
    else:break
df = pd.DataFrame(table_data, columns=['Links'])
excel_filename = 'links102_178.xlsx'
df.to_excel(excel_filename, index=False)
print(df)