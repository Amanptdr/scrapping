from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

def run():
        all_data = []
        driver1 = webdriver.Chrome()
        driver2 = webdriver.Chrome()
        time.sleep(1)
        driver1.get("https://dfpi.ca.gov/enf-p/")
        # time.sleep(2)
        table_data = WebDriverWait(driver1, 35).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table-striped")))
        # time.sleep(2)
        tbody = WebDriverWait(table_data, 35).until(
        EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        count = 1
        # time.sleep(0.5)
        for j in tbody.find_elements(By.TAG_NAME, "tr"):
        # print("35",j.find_elements(By.TAG_NAME, "td"))
        
        # driver1.maximize_window()
                time.sleep(1)
                sub = j.find_elements(By.TAG_NAME, "td")[0].text.strip()
                order = j.find_elements(By.TAG_NAME, "td")[1].text.strip()
                issue_date = j.find_elements(By.TAG_NAME, "td")[2].text.strip()
                td = WebDriverWait(j, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "td")))
                time.sleep(4)
                try:
                        link = WebDriverWait(td, 55).until(
                        EC.presence_of_element_located((By.TAG_NAME, "a")))
                        print("49",link.get_attribute("href"))
                        if ".pdf" in link.get_attribute("href"):
                                data = {
                                "Subject":sub,
                                "Order Issued":order,
                                "Date Issued":issue_date,
                                "Document Link":link.get_attribute("href"),
                                "License or Case Number":"",
                                "Date of Initial Action":"",
                                "Defendants/Respondents":"",
                                "Documents":""
                                }
                        else:
                                print("61",link.get_attribute("href"))
                                time.sleep(1)
                                driver2.get(link.get_attribute("href"))
                                
                                # print("63",link.get_attribute("href"))
                                # time.sleep(0.5)
                                basic_detail = WebDriverWait(driver2, 45).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "et_pb_column_0")))
                                # time.sleep(1)
                                basic_data = WebDriverWait(basic_detail, 25).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "et_pb_text_0")))
                                for k in basic_data.find_elements(By.TAG_NAME, "p"):
                                        split_data = k.text.split(":")
                                        if split_data[0] == "License or Case Number":
                                                try:
                                                        case_num = str(split_data[1]).strip() + str(split_data[2]).strip()
                                                except:
                                                        case_num = str(split_data[1]).strip()
                                                # print("51",case_num)
                                        if split_data[0] == "Date of Initial Action":
                                                date = str(split_data[1]).strip()
                                                # print("54",date)
                                        if split_data[0] == "Defendants/Respondents":
                                                respo = str(split_data[1]).strip()
                                                # print("57",respo)
                                div_data = WebDriverWait(driver2, 65).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "et_pb_text_inner")))
                                time.sleep(1)
                                ul =  WebDriverWait(div_data, 65).until(
                                EC.presence_of_element_located((By.TAG_NAME, "ul")))
                                doc_arr = []
                                for l in ul.find_elements(By.TAG_NAME, "li"):
                                        print("80",link.get_attribute("href"))
                                        time.sleep(1)
                                        try:
                                                anchor = WebDriverWait(l, 75).until(
                                                EC.presence_of_element_located((By.TAG_NAME, "a")))
                                                print(anchor)
                                                doc_arr.append(anchor.get_attribute("href"))
                                        except:
                                                pass
                                docu = ", ".join(doc_arr)
                                data = {
                                "Subject":sub,
                                "Order Issued":order,
                                "Date Issued":issue_date,
                                "Document Link":"",
                                "License or Case Number":case_num,
                                "Date of Initial Action":date,
                                "Defendants/Respondents":respo,
                                "Documents":docu
                                }
                except:
                      data = {
                                "Subject":sub,
                                "Order Issued":order,
                                "Date Issued":issue_date,
                                "Document Link":"",
                                "License or Case Number":"",
                                "Date of Initial Action":"",
                                "Defendants/Respondents":"",
                                "Documents":""
                                }
                all_data.append(data)
                print("count", count)
                count += 1
        driver1.quit()
        driver2.quit()
        df = pd.DataFrame(all_data)
        df.to_excel("California_Department_of_Business_Oversight(DBO)_Actions_And_Orders_part-p.xlsx", index = False)
run()
