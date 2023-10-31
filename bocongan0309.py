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
checkFirst = True

def getHeaderData():
    print('header dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    res = requests.get('http://vpcqcsdt.bocongan.gov.vn/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3/ctl/chitiet/mid/1088/ma/d8240214-eef2-4c58-8202-99387fe818cd?returnUrl=/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3')
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find("table")
    one_row_data = []
    for row in table.find_all('tr'):
        for th in row.find_all('th'):
            text_to_translate = th.text.strip()
            try:
                translated_text = translator.translate(text_to_translate, src='vi', dest='en')
                table_headers.append(translated_text.text)
            except:
                table_headers.append(text_to_translate)
getHeaderData()
def getDataByBeutifulShop(link):
    print("start Third Step ----------33333333333333333333333333333333333")
    res = requests.get(link)
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find("table")
    one_row_data = []
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
                    one_row_data.append(translated_text.text)
                except:
                    one_row_data.append(text_to_translate)
                total = total-1
    table_data.append(one_row_data)


def getPageData():
    table = driver.find_element(By.XPATH, '//table')
    soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
    print("start Second Step ----------222222222222222222222222222222222222222222")
    for row in soup.find_all('tr'):
        second_td = row.find_all('td')
        for td in second_td:
            link_element = td.find('a')
            if link_element:
                link = link_element.get('href')
                print("Link:LinkLinkLinkLinkLinkLinkLinkLink", link)
                getDataByBeutifulShop(link)
                break
            else:
                print("No link found in the second <td>.")
pageNo = 0
while True:
    print("start first Step ----------1111111111111111111111111111111111111111111111111111")
    page_table = driver.find_element(By.XPATH, '//*[@id="dnn_ctr1088_ModuleContent"]/table')
    page_rows = page_table.find_elements(By.TAG_NAME, 'tr')
    for row in page_rows:
        last_td = row.find_elements(By.TAG_NAME, 'td')[-2]
        last_td_xpath = driver.execute_script("return arguments[0].getAttribute('xpath')", last_td)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, str(last_td_xpath))))
    except Exception as e:
        print(f"Error waiting for element: {e}")
        # break
    if last_td.is_enabled() and pageNo<179:
        if pageNo==0:
            pass
        else:
            last_td.click()
        getPageData()
        pageNo+=1
        if pageNo == 50 or pageNo == 100:
            try:
                df = pd.DataFrame(table_data, columns=table_headers)
                excel_filename = 'web_scraped_data_pagination11111111111111111111.xlsx'
                df.to_excel(excel_filename, index=False)
            except Exception as e:
                print("erro occured:")
        if(page==179):break
    else:break
df = pd.DataFrame(table_data, columns=table_headers)
excel_filename = 'web_scraped_data_final_list.xlsx'
df.to_excel(excel_filename, index=False)


# data = [
#     ['Alice', 25, 'New York'],
#     ['Bob', 30, 'San Francisco'],
#     ['Charlie', 35, 'Los Angeles'],
#     ['David', 28, 'Chicago']
# ]
# columns = ['Name', 'Age', 'City']
# df = pd.DataFrame(data, columns=columns)
# print(df)