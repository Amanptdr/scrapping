# import requests
# from bs4 import BeautifulSoup
# import time
# import json
# import pandas as pd
# linkArr = []
# mainData=[]

# def scrape_data(url):
#   objectData = {}
#   List1=[]
#   List2=[]
#   try:
#     response = requests.get(url)
#     details = BeautifulSoup(response.text, 'html.parser')
#     element = details.find(class_="formcon")
#     for dt in element.find_all("dt"):
#       List1.append(dt.text.strip())
#     for dd in element.find_all("dd"):
#       List2.append(dd.text.strip())
#     objectData = {k: v for k, v in zip(List1, List2)}
#     objectData['Links'] = url
#     print(objectData)
#     mainData.append(objectData)
#   except:
#     mainData.append({'Name':'','Company':'',"Address":'','Telephone':'','Links':url})
#     print("Something went wrong")
#   finally:
#     print("The 'try except' is finished")
#   time.sleep(1)

# url = "https://www.insolvencydirect.bis.gov.uk/fip1/Home/Search"
# payload = {}
# headers = {}
# response = requests.request("GET", url, headers=headers, data=payload)
# pageData = BeautifulSoup(response.text, 'html.parser')
# tbody = pageData.find('table')
# trs = pageData.find_all('tr')  # Set recursive=False to only consider direct children

# # for td in trs:
# #   print(td)


# scrape_data("https://www.insolvencydirect.bis.gov.uk/fip1/Home/IP/8733")
# # df = pd.DataFrame(linkArr, columns=['Links'])
# # excel_filename = 'insolvencyLinks.xlsx'
# # df.to_excel(excel_filename, index=False)


# df1 = pd.DataFrame(mainData)
# excel_file_path = 'insolvencyData.xlsx'
# df1.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
# print(f"Excel file '{excel_file_path}' created successfully.")




# https://www.fca.org.uk/news/warnings/brenner-and-associates



import pandas as pd
from bs4 import BeautifulSoup
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec  
from selenium.webdriver.common.action_chains import ActionChains
import time

all_data = []

# def getDataFun(all_tr):
#   # url = "https://www.insolvencydirect.bis.gov.uk/fip1/Home/Search"
#   # payload = {
#   #     'IPForename': '',
#   #     'IPSurname': '',
#   #     'IPCompany': '',
#   #     'IPTown': '',
#   #     'IPNumber': '',
#   #     'IPCounty': ''
#   #     }
#   # # response = requests.post(url, data=payload)
#   # response= requests.post(url, data=payload)
#   # soup = BeautifulSoup(response.text, 'html.parser')
#   # table = soup.find("table",{"class":"markuptable"})
#   # all_tr = table.find_all("tr")[1:]
#   for i in all_tr:
#     try:
#       columns = i.find_all('td')  
#       name = columns[0]
#       company = columns[1].text.strip()
#       responses = requests.get("https://www.insolvencydirect.bis.gov.uk"+name.find("a")["href"])
#       soups = BeautifulSoup(responses.text, 'html.parser')
#       main_div = soups.find("div", {"class":"formcon"})
#       dd_elements = main_div.select('div.formcon dd')
#       data = {
#           "Name":dd_elements[0].text,
#           "Company":dd_elements[1].text,
#           "Address":dd_elements[2].text,
#           "Telephone":dd_elements[3].text,
#           "Fax":dd_elements[4].text,
#           "IP Number":dd_elements[5].text,
#           "Licensing Body":"https://www.insolvencydirect.bis.gov.uk/" + dd_elements[6].find("a")["href"],
#           "Email":dd_elements[7].text,
#       }
#     except:
#       print("---------------------------something went Wrong----------------------------")
#       data={"Name":'',"Company":'',"Address":'',"Telephone":'',"Fax":'',"IP Number":'',"Licensing Body":'',"Email":'',"Link":"https://www.insolvencydirect.bis.gov.uk"+name.find("a")["href"]}
#     all_data.append(data)
# getDataFun()


driver = webdriver.Chrome()
driver.get("https://www.insolvencydirect.bis.gov.uk/fip1/Home/Search")
while True:
    # Scrape data from the current page
    # (use driver.find_element or driver.find_elements to locate elements)

    # Click the "Next" button or handle pagination
    page_table = driver.find_element(By.XPATH, '//*[@id="Content"]/div/table')
    page_rows = page_table.find_elements(By.TAG_NAME, 'tr')
    print(page_rows)
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="Content"]/div/a[4]')
        next_button.click()

        # Wait for the new page to load, adjust the timeout as needed
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//your-element-on-the-new-page")))
    except Exception as e:
        # No "Next" button found or other exception, exit the loop
        break
    break

driver.quit()

df = pd.DataFrame(all_data)
df.to_excel("insolvency_service.xlsx", index=False)