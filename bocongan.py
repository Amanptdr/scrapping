from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from time import sleep
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


# Configure the web driver (change to your preferred browser)
url = "http://vpcqcsdt.bocongan.gov.vn/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3"
# Navigate to the website with pagination
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 5)
# table = driver.find_elements(By.XPATH, '//*[@id="dnn_ctr1088_MainForm_palTruyna"]/table/tbody')
table = driver.find_element(By.XPATH, "//table")
# rows = table.find_element(By.XPATH, "//tr")
pagination = driver.find_element(By.XPATH,'//*[@id="dnn_ctr1088_ModuleContent"]/table/tbody/tr')
soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
page = BeautifulSoup(pagination.get_attribute('outerHTML'), "html.parser")
for p in page.find_all('td'):
    print(p.text.strip())
table_headers = []
for th in soup.find_all('th'):
    table_headers.append(th.text.strip())

table_data = []
def getPageData():
    table = driver.find_element(By.XPATH, "//table")
    soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
    for row in soup.find_all('tr'):
        columns = row.find_all('td')
        output_row = []
        for column in columns:
            output_row.append(column.text.strip())
        table_data.append(output_row)
pageNo = 1
while True:
    nextButton = driver.find_element(By.XPATH,'//*[@id="dnn_ctr1088_ModuleContent"]/table/tbody/tr/td[16]')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dnn_ctr1088_ModuleContent"]/table/tbody/tr/td[16]')))

    if nextButton.is_enabled() and pageNo<2:
        nextButton.click()
        getPageData()
        pageNo+=1
        print(nextButton,'==========',pageNo)
    else:
        break
    break

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