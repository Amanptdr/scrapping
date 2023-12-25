import requests
import pandas as pd
from bs4 import BeautifulSoup

fileData = []
url = "https://www.apra.gov.au/disqualification-register"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
page_source =BeautifulSoup(response.text, 'html.parser')
trs = page_source.find_all('table')[1].find('thead').find_all('tr')
trs.pop(0)
for item in trs:
  td_elements = item.find_all('td')
  if len(td_elements) == 7:
    last_name = td_elements[0].text.strip()
    first_name = td_elements[1].text.strip()
    disqualification_date = td_elements[2].text.strip()
    disqualification_power = td_elements[3].text.strip()
    effective_revocation_date = td_elements[4].text.strip()
    revocation_power = td_elements[5].text.strip()
    entity = td_elements[6].text.strip()
    
    fileData.append({
        "First name": first_name,
        "Last name": last_name,
        "Disqualification date": disqualification_date,
        "Disqualification power": disqualification_power,
        "Effective revocation date": effective_revocation_date,
        "Revocation power": revocation_power,
        "Entity": entity,
    })
df = pd.DataFrame(fileData)
excel_file_path = 'disqualifications-revoked.xlsx'
df.to_excel(excel_file_path, index=False) 
print(f"Excel file '{excel_file_path}' created successfully.")