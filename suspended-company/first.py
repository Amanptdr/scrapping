import requests
import json
import pandas as pd
fileData = []
def mainfun(page):
  url = "https://asx.api.markitdigital.com/asx-research/1.0/companies/directory?page="+str(page)+"&itemsPerPage=25&order=ascending&orderBy=companyName&marketCapBucket[]=Suspended&includeFilterOptions=false&recentListingsOnly=false"

  payload = {}
  headers = {
    # 'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozMzksImVtYWlsIjoiS3JpdGkuaGFyamlrYUBtYWNoYWRhbG8uY29tIiwidXNlcm5hbWUiOiJrcml0aWhhcmppa2ExIiwibmFtZSI6IktyaXRpIGhhcmppa2EiLCJleHAiOjE2OTg0ODc3ODYsIm9yaWdfaWF0IjoxNjk4NDAxMzg2fQ.TxeWgmhXayK8Db02isM8J205CG7gB9nxVNvpRWrZM8I'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  tableData = json.loads(response.text)
  for item in tableData['data']['items']:
    fileData.append({'ASX CODE':item['symbol'],'COMPANY NAME':item['displayName'],'INDUSTRY':item['industry'],'LIST DATE':item['dateListed'],'MARKET CAP':item['marketCap']})
  if len(fileData)!=tableData['data']['count']:
    mainfun(page+1)
# for i in range(4):
mainfun(0)
df = pd.DataFrame(fileData)
excel_file_path = 'company-data.xlsx'
df.to_excel(excel_file_path, index=False) 
print(f"Excel file '{excel_file_path}' created successfully.")