import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def getAmountFromText(text):
    match = re.search(r'\$([\d,]+)', text)
    if match:
        amount = match.group(1)
        amount = int(amount.replace(',', ''))
        return "$"+str(amount)
    else:
        print("Amount not found.")
        return ''

url1  = "https://www.police.nsw.gov.au/can_you_help_us/rewards/50000_reward/disappearance_of_peter_messariti"
response1 = requests.request("GET",url1, headers={}, data={})
details = BeautifulSoup(response1.text, 'html.parser')
rowData={}
fileData = []
try:
    if len(details.find_all(class_="breadcrumbs__link")):
        rowData['reward offered for information'] = getAmountFromText(details.find_all(class_="breadcrumbs__link")[3].get_text(strip=True))
        rowData['Name'] = details.find('h2',class_="c-section-nav__title").get_text(strip=True) or ''
        p_tags = details.find(class_="o-content").find_all('p')
        rowData['Details'] = '\n'.join([p.get_text() for p in p_tags]) or ''
        if details.find(class_="o-content") and details.find(class_="o-content").find('img') and details.find(class_="o-content").find('img').get('src'):
            rowData['Images'] = details.find(class_="o-content").find('img').get('src')
        else:rowData['Images'] =''
    else:
        rowData['Name'] = ""
        rowData['Images'] = ""
        rowData['Details'] = url1
except:
  rowData['Name'] = ""
  rowData['Images'] = ""
  rowData['Details'] = url1
  print("---------------",url1,"-------------------------")
fileData.append(rowData)
print (fileData)
# import re
# url = "https://www.police.nsw.gov.au/can_you_help_us/rewards/350,000_reward_offered/suspected_murder_of_darren_royce_willis"

# # Define a regular expression pattern to match the number
# pattern = r'/\$(\d{1,3}(?:,\d{3})*)_reward_offered/'
#  pattern = r'(\d+)_reward'

# # Use re.search to find the match
# match = re.search(pattern, url)

# if match:
#     # Extract the matched number and remove any commas
#     amount = match.group(1).replace(",", "")
#     print("Amount:", amount)
# else:
#     print("Number not found in the URL.")