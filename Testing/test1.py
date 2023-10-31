import requests
from bs4 import BeautifulSoup
import pandas as pd
url="https://appointment.sec.gov.ph/lending-companies-and-financing-companies-2/list-of-revoked-and-suspended-lending-companies/"
res = requests.get(url)
soup = BeautifulSoup(res.text,'html.parser')
tables = soup.find_all("table")
headerList = list()
companyName = []
date = []
headerColumn = []

def createDataTable(index,mainHeader):
  data = []
  for row in tables[index].find_all('tr'):
    row_data = []
    for cell in row.find_all('td'):
      row_data.append(cell.text)
    data.append(row_data)
  for item in data:
    companyName.append(item[0])
    date.append(item[1])
count = 0
for header in soup.find_all(class_="accordion-title"):
  headerList.append(header.get_text())
  
for t in tables:
  createDataTable(count,headerList[count])
  count +=1
fileData = {"column1":'',"Column2":companyName,"Column3":date}
df= pd.DataFrame(fileData)
print(df)
df.to_csv("data1.csv")