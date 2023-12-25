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
    row_data = {}
    company_names = []
    authorisation_numbers = []
    soup_data = request_response(link)
    meta_data = soup_data.find("article").find(class_="accc-public-register-metadata").find_all(class_="field--label-inline")
    for item in meta_data:
      try:
        label = item.find('h3',class_="field__label").get_text(strip=True)
        value = item.find('div').get_text(strip=True)
        row_data[label] = value
      except:
        print(link)
    try:
      for company in soup_data.find(class_="field field--name-field-acccgov-applicants field--type-entity-reference-revisions field--label-above clearfix").find_all('li'):
        company_names.append(company.get_text(strip=True))
      row_data['Applicants'] = ' , '.join(company_names)
    except:
      row_data['Applicants'] = ''
    
    try:
      for number in soup_data.find(class_="field field--name-field-acccgov-authorisation-nums field--type-string field--label-above clearfix").find_all('li'):
        authorisation_numbers.append(number.get_text(strip=True))
      row_data['Authorisation Number'] = ' , '.join(authorisation_numbers)
    except:
      row_data['Authorisation Number'] = ''

    try:
      for data in soup_data.find_all(class_="view-grouping"):
        header = data.find(class_="view-grouping-header").get_text(strip=True)
        pdf_links = []
        for tr in data.find("tbody").find_all("tr"):
          tds = tr.find_all("td")
          pdf_links.append(base_url+tds[0].find('a').get('href')+" "+"("+tds[1].get_text(strip=True)+")")
        row_data[header] = ' , '.join(pdf_links)
    except:
      pass

    try:
      row_data['Description of Conduct'] = soup_data.find(class_="field field--name-field-accc-body field--type-text-with-summary field--label-above clearfix text-formatted").find('div',class_="field__item").get_text(strip=True)
    except:
      pass
    data_List.append(row_data)
  final_data.extend(data_List)
  df = pd.DataFrame(data_List)
  excel_file_path = file_name
  df.to_excel(excel_file_path, index=False) 
  print(f"Excel file '{excel_file_path}' created successfully.")
# scrapp_data("https://www.accc.gov.au/public-registers/authorisations-and-notifications-registers/authorisations-register","Authorisations_register.xlsx")
scrapp_data("https://www.accc.gov.au/public-registers/authorisations-and-notifications-registers/exclusive-dealing-notifications-register","exclusive-dealing.xlsx")
# df = pd.DataFrame(final_data)
# excel_file_path = "all_data.xlsx"
# df.to_excel(excel_file_path, index=False) 
# print(f"Excel file '{excel_file_path}' created successfully.")