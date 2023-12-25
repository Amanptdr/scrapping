import requests
import pandas as pd
from bs4 import BeautifulSoup

fileData = []
url = "https://asic.gov.au/online-services/search-asic-s-registers/additional-searches/court-enforceable-undertakings-register"
payload = {}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
page_source =BeautifulSoup(response.text, 'html.parser')
# h2_data = {}
h2_elements = page_source.find(class_="text-page-wrapper").find_all('h2')
h2_elements.pop(0)
for h2_element in h2_elements:
    key = h2_element.get_text(strip=True)
    table_element = h2_element.find_next('table')
    print("--------------",key,"-----------------------")
    if table_element:
      for tr in table_element.find('tbody').find_all('tr'):
        rowData = {}
        tds = tr.find_all('td')
        rowData['year'] = key
        rowData['Section of Act'] = tds[0].get_text(strip=True)
        name_of_parties = ''
        media_urls = []
        # if len(tds[1].find_all('p')):
        for url in tds[1].find_all('a'):
          media_urls.append("https://asic.gov.au/"+url.get('href'))
          url.extract()
        rowData['Media release Links']  = ", ".join(media_urls)
        rowData['Name of parties']= tds[1].get_text(strip=True)
        download_copy_url = []
        if len(tds[2].find_all('a')):
          for link in tds[2].find_all('a'):
            download_copy_url.append(link.get('href'))
          rowData['Download a copy of CEU as a PDF']=", ".join(download_copy_url)
        else:
          rowData['Download a copy of CEU as a PDF']=''

        rowData['Date of Acceptance by ASIC'] = tds[len(tds)-1].get_text(strip=True)
        fileData.append(rowData)
df = pd.DataFrame(fileData)
excel_file_path = 'australian-security.xlsx'
df.to_excel(excel_file_path, index=False) 
print(f"Excel file '{excel_file_path}' created successfully.")