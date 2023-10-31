import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


fileData = []

def mainfun(page):
  print("------------------",page,"--------------------------------------")

  url = "https://apps.police.nsw.gov.au/missingpersonsenquiry/search.do?start="+str(page)
  response = requests.request("GET", url, headers={}, data={})
  pageData = BeautifulSoup(response.text, 'html.parser')
  table = pageData.find_all('table',class_="appBorder")[2]
  cookies = response.cookies
  headers = {
      'Cookie': '; '.join([f'{name}={value}' for name, value in cookies.items()]),
      # Add other headers if necessary
  }
  for link in table.find_all('a'):
    rowData = {}
    url1  = "https://apps.police.nsw.gov.au"+link.get('href')
    response1 = requests.request("GET",url1, headers=headers, data={})
    details = BeautifulSoup(response1.text, 'html.parser')
    personData = details.find('td',id="bodycontent")
    # https://apps.police.nsw.gov.au/missingpersonsenquiry/
    rowData['Image'] = 'https://apps.police.nsw.gov.au/missingpersonsenquiry/'+personData.find('img').get('src')
    tables = personData.find('table',class_="appBorder").find_all('table',class_="appBorder")
    ques1 = tables[0].find_all(class_='appQuestionTD')
    try:
      for question in ques1:
        result_element = question.find_next(class_="appResultTD")
        if result_element:
          question_text = question.get_text(strip=True)
          result_text = result_element.get_text(strip=True)
          rowData[question_text] = result_text
      ques2 = tables[1].find_all(class_='appQuestionTD')
      for question in ques2:
        result_element = question.find_next(class_="appResultTD")
        if result_element:
          question_text = question.get_text(strip=True)
          result_text = result_element.get_text(strip=True)
          rowData[question_text] = result_text
      rowData[tables[2].find(class_="appTextWhite").get_text(strip=True)] = tables[2].find(class_="appTextWhite").find_next('td').get_text(strip=True)
    except:
      rowData['link'] = link
      print("---------------------failed------------",link,"---------------")
    fileData.append(rowData)


urlForPage = "https://apps.police.nsw.gov.au/missingpersonsenquiry/search.do?start=0"
responseForPage = requests.request("GET", urlForPage, headers={}, data={})
forPage = BeautifulSoup(responseForPage.text, 'html.parser')
text = forPage.find('td',class_="searchResultsPageRange").get_text(strip=True)
myList = re.split('\s', text)
count = int(myList[-1])//10
if int(myList[-1]) % 10 != 0:
    count += 1
for i in range(count):
  mainfun(i*10)
  time.sleep(2)


# print(fileData)
df = pd.DataFrame(fileData)
excel_file_path = 'missing-person.xlsx'
df.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
print(f"Excel file '{excel_file_path}' created successfully.")
