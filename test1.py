import requests
from bs4 import BeautifulSoup
import pandas as pd
# def fetchAndSaveData(url,path):
#   r = requests.get(url)
#   print(r.text)
#   with open(path,"w") as f:
#     f.write(r.text)
url="https://appointment.sec.gov.ph/lending-companies-and-financing-companies-2/list-of-revoked-and-suspended-lending-companies/"

# fetchAndSaveData(url,"data/test1.html")
# with open('data/test1.html',"r") as f:
#   html_doc = f.read()
res = requests.get(url)
soup = BeautifulSoup(res.text,'html.parser')
tables = soup.find_all("table")
data = []
for row in tables[0].find_all('tr'):
    row_data = []
    for cell in row.find_all('td'):
        row_data.append(cell.text)
    data.append(row_data)
name = []
date = []
for item in data:
  name.append(item[0])
  date.append(item[1])
fileData = {data[0][0]:name,data[0][1]:date}
df= pd.DataFrame(fileData)
print(df)
df.to_csv("data1.csv")

# 22222222222222222222
# data = []
# for row in tables[1].find_all('tr'):
#     row_data = []
#     for cell in row.find_all('td'):
#         row_data.append(cell.text)
#     data.append(row_data)
# name = []
# date = []
# for item in data:
#   name.append(item[0])
#   date.append(item[1])
# fileData = {data[0][0]:name,data[0][1]:date}
# df= pd.DataFrame(fileData)
# print(df)
# # 33333333333333333333333
# data = []
# for row in tables[2].find_all('tr'):
#     row_data = []
#     for cell in row.find_all('td'):
#         row_data.append(cell.text)
#     data.append(row_data)
# name = []
# date = []
# for item in data:
#   name.append(item[0])
#   date.append(item[1])
# fileData = {data[0][0]:name,data[0][1]:date}
# df= pd.DataFrame(fileData)
# print(df)