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
count = 0

def createDataTable(index,mainHeader):
  check = False
  data = []
  for row in tables[index].find_all('tr'):
    row_data = []
    for cell in row.find_all('td'):
      # print(cell.text)
      row_data.append(cell.text)
    data.append(row_data)
  for item in data:
    # print(item[0])
    if(check):
      companyName.append(item[0])
      date.append(item[1])
      headerColumn.append("")
    else:
      companyName.append('')
      date.append('')
      headerColumn.append(mainHeader)
      check = True

for header in soup.find_all(class_="accordion-title"):
  headerList.append(header.get_text())
for t in tables:
  createDataTable(count,headerList[count])
  count +=1
fileData = {"column1":headerColumn,"Column2":companyName,"Column3":date}
df= pd.DataFrame(fileData)
df.to_csv("data2.csv")