from config import Config
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

def run():
    # try:
        url = "https://fcraonline.nic.in/fc1a_Satewise_old.aspx"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"webdriver.chrome.driver={ChromeDriverManager().install()}")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get(url)
        driver.implicitly_wait(10)
        dropdown = driver.find_element(By.ID, "up_year")
        all_dropdown = dropdown.text.split("\n")
        all_dropdown.pop(0)
        file_name = pd.DataFrame()

        for year in all_dropdown:
                driver.implicitly_wait(1)
                driver.get(url)
                driver.implicitly_wait(1)
                ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
                your_element = WebDriverWait(driver, 10,ignored_exceptions=ignored_exceptions)
                your_element.until(EC.presence_of_element_located((By.ID, "ddlyear")))
                select = Select(driver.find_element(By.ID, "ddlyear"))
                wait = WebDriverWait(driver, 10)
                wait.until(EC.element_to_be_clickable((By.ID, "ddlyear")))
                time.sleep(8)
                select.select_by_value(year.strip())
                print(year)
                time.sleep(5)
                driver.find_element(By.XPATH, '/html/body/form/section/div/div[2]/div/div/div/div/div[1]/input').click()
                source = driver.page_source
                soup = BeautifulSoup(source, "lxml")
                table_tag = soup.find("table", attrs={"id": "tblassoresult"})
                
                if table_tag == None:
                    column_names = ["File No.", "Association Name", "Address", "Nature"]  # Add your desired column names here
                    file_name = pd.DataFrame(columns=column_names)
                    file_name['Year'] = year.strip()
                else:
                    try:
                        data = pd.read_html(table_tag.prettify(),flavor='bs4')[0]
                        data['Year'] = year.strip()
                        file_name = pd.concat([file_name, data], ignore_index=True)
                    except:
                        pass
                
                time.sleep(1)
                if year.strip() == "2008":
                    break
                    
        
        
        file_name.to_csv('task21.csv', index=False)
        
        

    # except Exception as exe:
    #     print(exe)
    #     # error_logger(str(exe))
    #     return False

run()