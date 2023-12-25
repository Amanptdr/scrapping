import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

base_url = "https://www.accc.gov.au"

final_data = []
def request_response(url):
  response = requests.request("GET", url, headers={}, data={})
  return BeautifulSoup(response.text,'html.parser')

def update_pagination(url, new_page):

    parsed_url = urlparse(url)

    query_params = parse_qs(parsed_url.query)

    query_params['page'] = [str(new_page)]

    updated_query = urlencode(query_params, doseq=True)

    updated_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, updated_query, parsed_url.fragment))

    return updated_url

def scrapp_data(section_link,file_name="Testing.xlsx"):
  soup = request_response(section_link)
  view_all = soup.find(class_="attachment attachment-after")
  link_list = []
  data_List = []

  if view_all:
    pagination_html = request_response(base_url+view_all.find('a').get('href'))
    get_api_url = pagination_html.find('li',class_="page-item page-item--last").find('a').get('href')
    parse_result = urlparse(get_api_url)
    total_pages = int(parse_qs(parse_result.query)['page'][0])
    
    for page in range(total_pages+1):
      print("--------------------page==",page,"---------------")
      url = update_pagination(base_url+"/public-registers/browse-public-registers"+get_api_url,page)
      response = requests.request("GET", url, headers={}, data={})
      soup = BeautifulSoup(response.text,'html.parser')
      for link in soup.find_all(class_="accc-card__inner"):
        link_list.append(base_url+link.find('a').get('href'))
  else:
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
          company_obj['Reference number'] = soup_data.find(class_="field field--name-field-acccgov-ref-number field--type-string field--label-inline clearfix").find(class_="field__item").get_text(strip=True)
        except:
          company_obj['Reference number'] = ""
        
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
  final_data.extend(data_List)
  df = pd.DataFrame(data_List)
  excel_file_path = file_name
  df.to_excel(excel_file_path, index=False) 
  print(f"Excel file '{excel_file_path}' created successfully.")
scrapp_data("https://www.accc.gov.au/public-registers/undertakings-registers/section-87b-undertakings-register","Section_87B_undertakings_register.xlsx")
scrapp_data("https://www.accc.gov.au/public-registers/undertakings-registers/section-93aa-undertakings-register","Section_93AA_undertakings_register.xlsx")
scrapp_data("https://www.accc.gov.au/public-registers/undertakings-registers/section-163-undertakings-register","Section_163_undertakings_register.xlsx")
scrapp_data("https://www.accc.gov.au/public-registers/undertakings-registers/general-undertakings-register","General_undertakings_register.xlsx")


df = pd.DataFrame(final_data)
excel_file_path = "all_data.xlsx"
df.to_excel(excel_file_path, index=False) 
print(f"Excel file '{excel_file_path}' created successfully.")