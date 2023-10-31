import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
def run():
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
                for i in range(6):
                    print(i,"38")
                    driver.execute_script("arguments[0].click()",loadMoreButton)
                    time.sleep(3)
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
            count = count + 1
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
                #         print('2222222222222',bb.findAll("div")[2].text)
                href = a.find("div", {"class": "slds-m-top_x-small"}).find(href=True)['href']
                time.sleep(2)
                driver.get(href)
                time.sleep(4)
                soup1 = BeautifulSoup(driver.page_source, "lxml")
                co = soup1.find("div", {"class": "slds-tabs_default"})
                ff = co.findAll('lightning-formatted-text')
                # import pdb;pdb.set_trace()
                counter = 0
                service =  ''
                for words in ff:
                    counter = counter + 1
                    print(words.getText())
                    if counter == 1:
                        name = words.getText()
                    if counter == 2:
                        Address = words.getText()
                    if counter == 3:
                        Mail_Address = words.getText()
                    if counter == 4:
                        Offsite_Cultivation_Address = words.getText()
                    if counter == 5:
                        Manufacture_Address = words.getText()
                    if counter == 6:
                        License = words.getText()
                    if counter == 7:
                        start_date = words.getText()
                    if counter == 8:
                        end_date = words.getText()
                    if counter == 9:
                        owner = words.getText()
                    if counter == 10:
                        service = words.getText()
                    # else:
                        # service=''
                try:
                    ff2 = co.findAll('lightning-formatted-rich-text')
                    service = ff2[0].text
                except:
                    service = ''
                row_dict = {
                    'remarks': remarks,
                    'alias': alias,
                    'name': name,
                    'Address': Address,
                    'href': href,
                    #                     "Offsite_Cultivation_Address":Offsite_Cultivation_Address,
                    #                     "Manufacture_Address":Manufacture_Address,
                    'License': License,
                    'start_date': start_date,
                    'end_date': end_date,
                    'owner': owner,
                    'service': service
                }

                df = df.append(row_dict, ignore_index=True)
                if Mail_Address:
                    row_dict2 = {
                        'remarks': remarks,
                        'alias': alias,
                        'name': name,
                        'Address': Mail_Address,
                        'href': href,
                        #                     "Offsite_Cultivation_Address":Offsite_Cultivation_Address,
                        #                     "Manufacture_Address":Manufacture_Address,
                        'License': License,
                        'start_date': start_date,
                        'end_date': end_date,
                        'owner': owner,
                        'service': service
                    }
                    df = df.append(row_dict2, ignore_index=True)
                if Offsite_Cultivation_Address:
                    row_dict3 = {
                        'remarks': remarks,
                        'alias': alias,
                        'name': name,
                        'Address': Offsite_Cultivation_Address,
                        'href': href,
                        #                     "Offsite_Cultivation_Address":Offsite_Cultivation_Address,
                        #                     "Manufacture_Address":Manufacture_Address,
                        'License': License,
                        'start_date': start_date,
                        'end_date': end_date,
                        'owner': owner,
                        'service': service
                    }
                    df = df.append(row_dict3, ignore_index=True)
                if Manufacture_Address:
                    row_dict4 = {
                        'remarks': remarks,
                        'alias': alias,
                        'name': name,
                        'Address': Manufacture_Address,
                        'href': href,
                        #                     "Offsite_Cultivation_Address":Offsite_Cultivation_Address,
                        #                     "Manufacture_Address":Manufacture_Address,
                        'License': License,
                        'start_date': start_date,
                        'end_date': end_date,
                        'owner': owner,
                        'service': service
                    }
                    df = df.append(row_dict4, ignore_index=True)
                    # import pdb;pdb.set_trace()
                driver.close()
            except AttributeError:
                print(count)
                print('@@@@@@@@@')
        # driver.close()
        df = df[df['Address'] != ' ']
        df.reset_index(inplace=True, drop=True)
        df["country"] = df["Address"].apply(lambda x: x.rsplit(",", 2)[-2] if x != '' else '')
        df["street"] = df["Address"].apply(lambda x: x.rsplit(",", 2)[-3] if x != '' else '')
        df["Address_zip_pr"] = df["Address"].apply(lambda x: x.rsplit(",", 2)[-1].split(" ") if x != '' else '')
        df["province"] = df["Address_zip_pr"].apply(lambda x: x[-2] if x != '' else '')
        df["postal code"] = df["Address_zip_pr"].apply(lambda x: x[-1] if x != '' else '')
        df.to_csv('az.csv', index=False)

    except Exception as exe:
        print(exe)
        print("Error")

run()
