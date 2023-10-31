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

translator = Translator()
# Configure the web driver (change to your preferred browser)
url = "http://vpcqcsdt.bocongan.gov.vn/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3"
# Navigate to the website with pagination
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 1)
# table = driver.find_elements(By.XPATH, '//*[@id="dnn_ctr1088_MainForm_palTruyna"]/table/tbody')
table = driver.find_element(By.XPATH, "//table")
# rows = table.find_element(By.XPATH, "//tr")
pagination = driver.find_element(By.XPATH,'//*[@id="dnn_ctr1088_ModuleContent"]/table/tbody/tr')
soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
page = BeautifulSoup(pagination.get_attribute('outerHTML'), "html.parser")
# for p in page.find_all('td'):
#     print(p.text.strip())
table_headers = []
for th in soup.find_all('th'):
    text_to_translate = th.text.strip()
    translated_text = translator.translate(text_to_translate, src='vi', dest='en')
    table_headers.append(translated_text.text)
table_data = []
def getPageData():
    table = driver.find_element(By.XPATH, "//table")
    soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
    for row in soup.find_all('tr'):
        print(",TABLESSSSSSSSSSSSSSS")
        columns = row.find_all('td')
        output_row = []
        checkFirst = True
        for column in columns:
            try:
                if checkFirst:
                    output_row.append(column.text.strip())
                    checkFirst = False
                else:
                    text_to_translate = column.text.strip()
                    translated_text = translator.translate(text_to_translate, src='vi', dest='en')
                    output_row.append(translated_text.text)
            except:
                output_row.append('')
        table_data.append(output_row)
pageNo = 0
while True:
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
        # print(last_td,'==========',pageNo)
        if(page==179):break
    else:break
print("successss,1111111111111111111111111111111")
df = pd.DataFrame(table_data, columns=table_headers)
excel_filename = 'web_scraped_data.xlsx'
df.to_excel(excel_filename, index=False)





# data_list = []
# for row in table.find_elements(By.XPATH,'//tr'):
#     row_data = [cell.text.strip() for cell in row.find_elements(By.XPATH,'//td')]
#     data_list.append(row_data)
#     break
# df = pd.DataFrame(data_list, columns=['STT', 'Họ tên đối tượng', 'Năm sinh','Nơi ĐKTT','Họ tên bố/mẹ','Tội danh','Số ngày QĐ' 'Đơn vị ra QĐTN'])        
# excel_filename = 'web_scraped_data.xlsx'
# df.to_excel(excel_filename, index=False)


# data = [
#     ['Alice', 25, 'New York'],
#     ['Bob', 30, 'San Francisco'],
#     ['Charlie', 35, 'Los Angeles'],
#     ['David', 28, 'Chicago']
# ]
# columns = ['Name', 'Age', 'City']
# df = pd.DataFrame(data, columns=columns)
# print(df)