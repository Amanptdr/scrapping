import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
linkArr = []
mainData=[]

def scrape_data(url):
  objectData = {}
  try:
    response = requests.get(url)
    details = BeautifulSoup(response.text, 'html.parser')
    element = details.find(id=['content-container'])
    objectData['company'] = element.find('h1').text.strip() if element.find('h1').text.strip() else ''
    for item in element.find(class_='grid-row').find_all('dl'):
      print(item.find('dt').text.strip(),"-------------", item.find('dd').text.strip())
      objectData[item.find('dt').text.strip()] = item.find('dd').text.strip() if item.find('dd').text.strip() else ""
    objectData['Disqualifications'] = element.find(class_='disqualification').find('h2').text.strip() if element.find(class_='disqualification').find('h2').text.strip() else ''
    for item in element.find(class_='disqualification').find_all('dl'):
      if item.find('dt').text.strip():
        objectData[item.find('dt').text.strip()] = item.find('dd').text.strip() if item.find('dd').text.strip() else ""
    print(objectData)
    # heading = element.find_all('h2')
    # objectData['heading'] = heading[0].text.strip()
    # pTags = element.find_all('p')
    # discription = ''
    # for item in pTags:
    #   strong = item.find('strong')
    #   if strong:
    #     key = strong.text.strip()[:-1]
    #     value = strong.find_next_sibling(text=True).strip()
    #     objectData[key] = value
    #   else:
    #     child_tags = item.find_all()
    #     h2_tag = item.find_previous('h2')
    #     if not child_tags and not h2_tag:
    #       discription = discription+item.text.strip()
    # objectData['reviews'] = discription
    # objectData['Links'] = url
    # mainData.append(objectData)
    print('------------------------',url,'--------------------------')
  except Exception as e:
    print("------------------",e,'--------------------')
    mainData.append({'company':'',"Disqualifications":'','Links':url})
    print("Something went wrong")
  finally:
    print("The 'try except' is finished")
  time.sleep(1)


for page in range(1,11):
  url = "https://find-and-update.company-information.service.gov.uk/register-of-disqualifications/A?page="+str(page)
  payload = {}
  headers = {
  'Cookie': '__SID=Pa5M91ZXmNZsKFvYvk49D8dfy+YZWaiUuZSvpXXJXo4NpXDPp/P6bI4'
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  # json_object = json.loads(response.text)
  pageData = BeautifulSoup(response.text, 'html.parser')
  table = pageData.find('table')
  for tr in table.find_all('tr')[1:]:
    link_element = 'https://find-and-update.company-information.service.gov.uk/'+tr.find("td").find('a').get('href')
    scrape_data(link_element)
    linkArr.append(link_element)
  time.sleep(3)
  # for td in tbody.find_all(class_="views-field views-field-letter"):
  #   link_element = 'https://find-and-update.company-information.service.gov.uk/'+td.find('a').get('href')
  #   scrape_data(link_element)
  #   linkArr.append(link_element)
  #   time.sleep(3)
df = pd.DataFrame(linkArr, columns=['Links'])
excel_filename = 'companyInformationLink.xlsx'
df.to_excel(excel_filename, index=False)


df1 = pd.DataFrame(mainData)
excel_file_path = 'companyInformation.xlsx'
df1.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
print(f"Excel file '{excel_file_path}' created successfully.")
