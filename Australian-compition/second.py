import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs



url = "https://www.accc.gov.au/public-registers/browse-public-registers?f%5B0%5D=type%3Aacccgov_infringement_notice&page=0"
response = requests.request("GET", url, headers={}, data={})
pageData = BeautifulSoup(response.text, 'html.parser')
pagination = pageData.find(class_="pagination justify-content-center").find_all('li')[-1].find('a').get('href')
parse_result = urlparse(pagination)
totalpage = int(parse_qs(parse_result.query)['page'][0])
print(dict_result)