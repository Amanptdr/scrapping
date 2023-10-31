import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
def run():
    mainData = []
    try:
        # create_audit(source_dict, 'Scrapping')
        # log_fname = make_directory(source_dict)
        # chrome_options = chrome_options_configuration(log_fname)
        driver = webdriver.Chrome()
        # url = 'https://azcarecheck.azdhs.gov/s/?facilityId=001t000000L0TAWAA3&facilityType=Marijuana+Establishment'
        url = 'https://azcarecheck.azdhs.gov/s/'
        driver.get(url)
        # import pdb;pdb.set_trace()
        time.sleep(10)
        while True:
            try:
                loadMoreButton = driver.find_element(By.XPATH,"//button[contains(text(),'Load More')]")
                # time.sleep(2)
                for i in range(1):
                    print(i,"38")
                    driver.execute_script("arguments[0].click()",loadMoreButton)
                    time.sleep(2)
                break
            except Exception as e:
                print(e)
                break
        soup = BeautifulSoup(driver.page_source, "lxml")
        rows2 = soup.find("div", {"class": "slds-scrollable_y"})
        df = pd.DataFrame(columns=['name', 'remarks', 'alias', 'Address', 'License', 'start_date', 'end_date', 'owner',
                                   'service','href'])  # 'Mail_Address','Offsite_Cultivation_Address','Manufacture_Address',
        count = 0
        for i in rows2:
            rowObject = {}
            count = count + 1
            print("--------------------",count,"--------------------------")
            try:
                driver = webdriver.Chrome()
                a = i.find("div", {"class": "slds-media slds-media_center"})
                bb = a.find("div", {"class": "slds-media__body"})
                
                op_or_not = bb.findAll("div")[2].text
                alias = bb.findAll("div")[0].text
                if 'Not Operating' in op_or_not:
                    remarks = 'Not Operating'
                else:
                    remarks = 'Operating'
                rowObject['remarks'] = remarks
                href = a.find("div", {"class": "slds-m-top_x-small"}).find(href=True)['href']
                time.sleep(1)
                driver.get(href)
                time.sleep(2)
                soup1 = BeautifulSoup(driver.page_source, "lxml")
                details = soup1.find('div',{"class":'slds-scrollable_y'})
                list1 = details.find(class_="slds-slot").find_all(class_="slds-size_12-of-12 slds-small-size_12-of-12 slds-large-size_6-of-12")
                # co = soup1.find("div", {"class": "slds-tabs_default"})
                # ff = co.findAll('lightning-formatted-text')
                for item in list1:
                    for paragraph in item.find_all(["p"]):
                        key  = paragraph.text.strip()
                        next_sibling = paragraph.find_next_sibling()
                        try:   
                           link = next_sibling.get('href')
                        except:
                            link = ""
                        value = next_sibling.text.strip() if next_sibling else ""
                        # if link =="":
                        #     value = next_sibling.text.strip() if next_sibling else ""
                        # else:
                        #     value = next_sibling.text +" ("+ str((link))+")" if next_sibling else ""
                        rowObject[key] = value
                mainData.append(rowObject)
                driver.close()
            except AttributeError:
                mainData.append({"Legal Name":"","Link":href,"Address":'',"Mailing Address":'',"License":""})
                print("-----------------eeeeeeeeeeeeeeeee---------------",count)
                print("errrrrrrrrrrrrrrorrrrrrrrrrrrrrrrrrr")
        df = pd.DataFrame(mainData)
        excel_file_path = 'mainData1.xlsx'
        df.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
        print(f"Excel file '{excel_file_path}' created successfully.")

    except Exception as exe:
        print('----------------',exe,'----------------------------')
run()
