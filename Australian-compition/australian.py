import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
# https://www.accc.gov.au/public-registers/undertakings-registers/section-87b-undertakings-register
# https://www.accc.gov.au/public-registers/undertakings-registers/section-93aa-undertakings-register
# https://www.accc.gov.au/public-registers/undertakings-registers/section-163-undertakings-register
# https://www.accc.gov.au/public-registers/undertakings-registers/general-undertakings-register

base_url = "https://www.accc.gov.au"
url = "https://www.accc.gov.au/public-registers/browse-public-registers?f%5B0%5D=type%3Aacccgov_undertaking&f%5B1%5D=acccgov_undertaking_type%3A509&page=0"
response = requests.request("GET", url, headers={}, data={})
soup = BeautifulSoup(response.text,'html.parser')
link_list = []
data_List = []

parse_result = urlparse(soup.find('li',class_="page-item page-item--last").find('a').get('href'))
total_pages = int(parse_qs(parse_result.query)['page'][0])

for page in range(total_pages+1):
  print("--------------------page==",page,"---------------")
  url = f"https://www.accc.gov.au/public-registers/browse-public-registers?f%5B0%5D=type%3Aacccgov_undertaking&f%5B1%5D=acccgov_undertaking_type%3A509&page={str(page)}"
  response = requests.request("GET", url, headers={}, data={})
  soup = BeautifulSoup(response.text,'html.parser')
  for link in soup.find_all(class_="accc-card__inner"):
    link_list.append(base_url+link.find('a').get('href'))

for link in link_list:  
    res = requests.request("GET", link, headers={}, data={})
    soup_data = BeautifulSoup(res.text,'html.parser')
    number_of_companies = soup_data.find("article").find("ul",class_="field__items").find_all("li")
    company_arr = []
    for data in number_of_companies:
      company_obj = {}
      for item in data.find_all('div', class_='field__item'):
        label = item.find_previous('h3', class_='field__label').get_text(strip=True)
        value = item.text.strip()
        company_obj[label] = value
        try:
          company_obj['Undertaking date'] = soup_data.find(class_="field field--name-field-acccgov-pub-reg-date field--type-datetime field--label-inline clearfix").find("time").get_text(strip=True)
        except:
          company_obj['Undertaking date'] = ''
        
        try:
          company_obj['Undertaking End date'] = soup_data.find(class_="field field--name-field-acccgov-undertakin-end-dat field--type-datetime field--label-inline clearfix").find('time').get_text(True)
        except:
          company_obj['Undertaking End date'] = ''
        
        try:
          company_obj['Undertaking type'] =soup_data.find(class_="field field--name-field-acccgov-undertaking-type field--type-entity-reference field--label-inline field--type-entity-reference--taxonomy_term clearfix").find(class_="field__item").get_text(strip=True)
        except:
          company_obj['Undertaking type'] = ''
        
        try:
          company_obj['Section'] =soup_data.find(class_="field field--name-field-acccgov-undertaking-sectio field--type-string field--label-inline clearfix").find(class_="field__item").get_text(strip=True)
        except:
          company_obj['Section'] = ''
        
        try:
          company_obj['Industry'] = soup_data.find(class_="field field--name-field-acccgov-industry field--type-string field--label-inline clearfix").find(class_="field__item").get_text(strip=True)
        except:
          company_obj['Industry'] =''
        
        try:
          company_obj['Undertaking'] = soup_data.find(class_="field field--name-field-accc-body field--type-text-with-summary field--label-above clearfix text-formatted") and soup_data.find(class_="field field--name-field-accc-body field--type-text-with-summary field--label-above clearfix text-formatted").find(class_="field__item").get_text(strip=True)
        except:
          company_obj['Undertaking'] = ""

      company_arr.append(company_obj)
    for data in company_arr:
      if data != {}:
        data_List.append(data)
df = pd.DataFrame(data_List)
excel_file_path = 'Section_87B_undertakings_register.xlsx'
df.to_excel(excel_file_path, index=False) 
print(f"Excel file '{excel_file_path}' created successfully.")