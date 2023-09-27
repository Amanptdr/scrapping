import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import xlsxwriter
workbook = xlsxwriter.Workbook('negara_bank3.xlsx')
worksheet = workbook.add_worksheet()

column_names = [
    'Name of unauthorised entities/individual',
    'Main website',
    'Facebook website',
    'Telegram website',
    'Date Added to Alert List'
]

for col_num, col_name in enumerate(column_names):
    worksheet.write(0, col_num, col_name)

row = 1


url = "https://www.bnm.gov.my/have-you-seen"
driver = webdriver.Chrome()
driver.get(url)
sleep(1)
table = driver.find_elements(By.XPATH, '/html/body/section[2]/div/div/div[1]/div/div[2]/section/div/div[2]/div/div/div/section/div/div/div')
# sleep(7)
# print("33")
data_list = []
for i in table:
    sleep(10)
    # print("36")
    aaa  = i.find_elements(By.XPATH, '//*[@id="portlet_com_liferay_journal_content_web_portlet_JournalContentPortlet_INSTANCE_NORWD0zlb5tE"]/div/div[2]/div/div/div/section/div/div/div/div')
    sleep(8)
    aa = []
    for j in aaa:
        # print(j.text)
        sleep(7)
        # print()
        aa.append(j.text)
    # print(aa)
    for k in aa:
        wwer = k.strip().split("\n")
        # print(wwer)
        passport = ''
        age = ''
        nation = ''
        address = ''
        bb = []
        for l in wwer:
            if wwer.count("Name ") >1:
                print(wwer)
            # print(l)
            # bb.append(l)
        # print(bb)
            if "Name" in l:
                name = l.split(":")[1]
            else:
                if "Name" in wwer[1]:
                    name =  wwer[1].split(":")[1]
                else:
                    name = wwer[1]
                    print(name)
            if "Passport No." in l:
                passport = l.split(":")[1]
            if "Age" in l:
                age = l.split(":")[1]
            if "Nationality" in l:
                nation = l.split(":")[1]
            if "Last Known address " in l:
                print(l)
                address = l.split(":")[1]
                if len(address) == 0:
                    index = wwer.index("Last known address")
                    address = wwer[index:wwer[-1]]
            else:
                if "Last address" in l:
                    address = l.split(":")[1]
                    if len(address) == 0:
                        index = wwer.index("Last known address")
                        address = wwer[index:wwer[-1]]
            # break
            row_data = {
                "Heading": wwer[0],
                "Name": name,
                "Passport No.": passport,
                "Age": age,
                "Nationality":nation,
                "Last known address":address,
                "Detail":wwer[-1]
            }

        data_list.append(row_data)
df = pd.DataFrame(data_list)
df.to_excel("negara_bank_malaysia2.xlsx", index=False)