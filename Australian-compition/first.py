import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs


fileData = []

def mainfun(page):

  url = "https://www.accc.gov.au/public-registers/browse-public-registers?f%5B0%5D=type%3Aacccgov_infringement_notice&page="+str(page)
  response = requests.request("GET", url, headers={}, data={})
  pageData = BeautifulSoup(response.text, 'html.parser')
  links = pageData.find(class_="view-content").find_all('a')
  for link in links:
    rowData = {}
    response = requests.get("https://www.accc.gov.au/"+link.get('href'))
    details = BeautifulSoup(response.text, 'html.parser')
    try:
      rowData['Heading'] = details.find(class_="field field--name-title field--type-string field--label-hidden").text.strip()
      arr = details.find('article').find(class_="accc-public-register-metadata").find_all(class_='field')
      for i in arr:
        key = i.find('h3').text.strip()
        value = i.find('div').text.strip()
        rowData[key] = value
      arr2 = details.find('article').find(class_="paragraph").find_all(class_='field')
      for j in arr2:
        key1 = j.find('h3').text.strip()
        value1 = j.find('div').text.strip()
        rowData[key1] = value1

      fileData.append(rowData)
      print("---------------------Success--------------")
    except:
      rowData['Heading']  = ""
      rowData['links'] = link
      print(link)
      print("---------------------failed--------------")

url1 = "https://www.accc.gov.au/public-registers/browse-public-registers?f%5B0%5D=type%3Aacccgov_infringement_notice&page=0"
response = requests.request("GET", url1, headers={}, data={})
soup = BeautifulSoup(response.text, 'html.parser')
pagination = soup.find(class_="pagination justify-content-center").find_all('li')[-1].find('a').get('href')
parse_result = urlparse(pagination)
totalpage = int(parse_qs(parse_result.query)['page'][0])

for page in range(totalpage+1):
  print("-------------------------------------",page,"----------------------------------")
  mainfun(page) 

df = pd.DataFrame(fileData)
excel_file_path = 'fileData.xlsx'
df.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
print(f"Excel file '{excel_file_path}' created successfully.")
