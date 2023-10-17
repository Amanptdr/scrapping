import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import json
mainData=[]
def scrape_data(url):
  try:
    # url = "https://www.fca.org.uk/news/warnings/fluentmoney-fluent-money-loan-lenders-clone-fca-authorised-firm"
    response = requests.get(url)
    objectData = {}
    details = BeautifulSoup(response.text, 'html.parser')
    element = details.find(id=['section-clone-firm-details','section-unauthorised-firm-details'])
    heading = element.find_all('h2')
    objectData['heading'] = heading[0].text.strip()
    pTags = element.find_all('p')
    discription = ''
    for item in pTags:
      strong = item.find('strong')
      if strong:
        key = strong.text.strip()[:-1]
        value = strong.find_next_sibling(text=True).strip()
        objectData[key] = value
      else:
        child_tags = item.find_all()
        h2_tag = item.find_previous('h2')
        if not child_tags and not h2_tag:
          discription = discription+item.text.strip()
    objectData['reviews'] = discription
    mainData.append(objectData)
    print('------------------------',url,'--------------------------')
  except:
    print("Something went wrong",url,"------------------")
  finally:
    print("The 'try except' is finished",url,"------------------")
    # df = pd.DataFrame(mainData)
    # excel_file_path = 'mainData.xlsx'
    # df.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
    # print(f"Excel file '{excel_file_path}' created successfully.")




excel_file = 'linksFca1.xlsx'  # Replace with your file name
sheet_name = 'Sheet1'  # Replace with your sheet name
df1 = pd.read_excel(excel_file, sheet_name=sheet_name)
df1['Scraped Data'] = df1['Links'].apply(scrape_data)


df = pd.DataFrame(mainData)
excel_file_path = 'mainData.xlsx'
df.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
print(f"Excel file '{excel_file_path}' created successfully.")

# data = [
#     {'Name': 'Alice', 'Age': 25, 'City': 'New York'},
#     {'Name': 'Bob', 'Age': 30, 'City': 'Los Angeles','id':"23434525"},
#     {'Name': 'Charlie', 'Age': 35, 'City': 'Chicago'},
# ]
# df = pd.DataFrame(data)
# excel_file_path = 'sample_data.xlsx'
# df.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers

# print(f"Excel file '{excel_file_path}' created successfully.")
