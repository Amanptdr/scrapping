import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

fileData = []
headers = {
        "Cookie":'_gcl_au=1.1.1839491023.1698671041; _gid=GA1.3.768787315.1698671041; cf_chl_2=11de2b6bacd0b66; cf_clearance=0G88yAs3rqWe3Q97x195qJdGE_loEc3_blnyJxPRdxg-1698734604-0-1-39cf5504.1c5ac447.c15f6658-160.0.0; _ga_BFRC85M34X=GS1.1.1698732529.4.1.1698735911.60.0.0; _ga=GA1.3.945726436.1698671041',
        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        "Authority":'www.crimestoppersvic.com.au'
    }
def mainfun(page):
  print("============",page,"----------------------")
  if page!=1:
    url = "https://www.crimestoppersvic.com.au/help-solve-crime/wanted-persons/banyule/"+str(page)+"/"
  else:
    url = "https://www.crimestoppersvic.com.au/help-solve-crime/wanted-persons/banyule/"
  response = requests.request("GET",url, headers=headers, data={})
  details = BeautifulSoup(response.text, 'html.parser')
  criminals = details.find_all('article',class_="elementor-grid-item")
  try:
    for crime in criminals:
      rowData = {}
      link = crime.find('a',class_='elementor-button elementor-button-link elementor-size-sm').get('href')
      response1 = requests.request("GET",link, headers=headers, data={})
      criminal_details = BeautifulSoup(response1.text, 'html.parser')
      sections = criminal_details.find('main').find_all('section')
      rowData['Name'] = sections[0].find('h2',class_="elementor-heading-title").get_text(strip=True)
      rowData['Reference'] = sections[0].find('h3',class_="elementor-heading-title").get_text(strip=True)[10:]
      # rowData['Last Seen'] = sections[0].find('h4',class_="elementor-heading-title").get_text(strip=True)[10:]
      rowData['Image'] = sections[1].find(class_="elementor-gallery-item").get('href')
      body_details = sections[1].find_all('h5',class_="elementor-heading-title")
      for detail in body_details:
        span = detail.find('span', style="color: #5e7387")
        if span:
          key = span.get_text(strip=True)
          value = detail.text.replace(key, "").strip()
          rowData[key] = value
        description = sections[1].find_all(class_="elementor-widget-text-editor")
        if description:
          desc_text = ""
          for disc in description:
            desc_text += disc.find(class_="elementor-widget-container").get_text(strip=True)
            rowData['remarks'] = desc_text
      fileData.append(rowData)
  except:
    rowData["Details"] = link
    fileData.append(rowData)

urlForPage = "https://www.crimestoppersvic.com.au/help-solve-crime/wanted-persons/banyule/"
responseForPage = requests.request("GET", urlForPage, headers=headers, data={})
forPage = BeautifulSoup(responseForPage.text, 'html.parser')
count = int(forPage.find_all('a',class_="page-numbers")[-2].get_text(strip=True).replace('Page',''))
for i in range(1,count+1):
  print(i)
  mainfun(i)
df = pd.DataFrame(fileData)
excel_file_path = 'criminals_2.xlsx'
df.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
print(f"Excel file '{excel_file_path}' created successfully.")