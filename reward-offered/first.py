import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

fileData = []

def getAmountFromText(text):
    match = re.search(r'\$([\d,]+)', text)
    if match:
        amount = match.group(1)
        amount = int(amount.replace(',', ''))
        return "$"+str(amount)
    else:
        print("Amount not found.")
        return ''


def mainfun():

  url = "https://www.police.nsw.gov.au/can_you_help_us/rewards"
  response = requests.request("GET", url, headers={}, data={})
  pageData = BeautifulSoup(response.text, 'html.parser')
  for item in pageData.find(class_="o-content").find_all(class_="p-photo-grid__link"):
    rowData = {}
    url1  = "https://www.police.nsw.gov.au/can_you_help_us/"+item.get('href')
    response1 = requests.request("GET",url1, headers={}, data={})
    details = BeautifulSoup(response1.text, 'html.parser')
    try:
      if len(details.find_all(class_="breadcrumbs__link")):
        rowData['reward offered for information'] = getAmountFromText(details.find_all(class_="breadcrumbs__link")[3].get_text(strip=True))
        rowData['Name'] = details.find('h2',class_="c-section-nav__title").get_text(strip=True) or ''
        p_tags = details.find(class_="o-content").find_all('p')
        rowData['Details'] = '\n'.join([p.get_text() for p in p_tags]) or ''
        if details.find(class_="o-content") and details.find(class_="o-content").find('img') and details.find(class_="o-content").find('img').get('src'):
          rowData['Images'] = details.find(class_="o-content").find('img').get('src')
        else:rowData['Images'] =''
      else:
        target_link = item.get('href')
        anchor_element = pageData.find('a', href=target_link)
        if anchor_element:
          previous_div = anchor_element.find_parent('div')
          if previous_div:
            print(anchor_element.find_parent('div').find_previous('div').find('h2').get_text(strip=True))
            rowData['reward offered for information'] = getAmountFromText(anchor_element.find_parent('div').find_previous('div').find('h2').get_text(strip=True))
          else:
            print("No previous div found")
        else:
          print("Link not found in the HTML")
        rowData['Name'] = item.find_all(class_="p-photo-grid__grid")[1].get_text(strip=True)
        rowData['Images'] = item.find_all(class_="p-photo-grid__grid")[0].find('img').get('src')
        rowData['Details'] = url1
        print("-----------------------SUCESSSS--------------------")
    except:
      rowData['Name'] = ""
      rowData['Images'] = ""
      rowData['Details'] = url1
      print("-----------------------",url,"--------------------ERORRRRRRR")
    fileData.append(rowData)
mainfun()
df = pd.DataFrame(fileData)
excel_file_path = 'reward-offered.xlsx'
df.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
print(f"Excel file '{excel_file_path}' created successfully.")
