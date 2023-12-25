import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
import time
import os
import glob


start_time = time.time()

mainData=[]

def decode_email(email_array):
  email_text =[]
  for email in email_array:
    encoded_email = email.get('data-cfemail')
    try:
      r = int(encoded_email[:2], 16)
      decoded_email = ''.join(
        [chr(int(encoded_email[i:i+2], 16) ^ r) for i in range(2, len(encoded_email), 2)]
        )
    except:
      decoded_email = ""
    email_text.append(decoded_email)
  email_text = ','.join(email_text)
  return email_text
count = 0
def scrape_data(url):
  global count
  count += 1
  objectData = {}
  find_by_class = False
  try:
    response = requests.get(url)
    details = BeautifulSoup(response.text, 'html.parser')
    element = details.find(id=['section-clone-firm-details','section-unauthorised-firm-details'])
    if element == None:
      element = details.find(class_="copy-block default")
      find_by_class = True
    heading = element.find_all(['h2','h3'])
    objectData['heading'] = heading[0].text.strip()
    pTags = element.find_all('p')
    discription = ''
    for item in pTags:
      strong = item.find('strong')
      if strong:
        key = strong.text.strip()[:-1]
        if key!='Email':
          value = strong.find_next_sibling(text=True).strip()
        else:
          email_arr = element.find_all(class_="__cf_email__")
          decoded_email = decode_email(email_arr) #item.find('a').get('data-cfemail')
          value = decoded_email
        objectData[key] = value
      else:
        if not find_by_class:
          a_tags = item.find_all('a', class_='__cf_email__')
          if not a_tags:
            discription = discription+item.text.strip()
    if find_by_class:
      h3_tag = element.find('h3')
      h2_tag = element.find('h2')
      p_tags_between_h3_h2 = []
      current_tag = h3_tag.find_next_sibling()
      while current_tag and current_tag.name != 'h2':
        if current_tag.name == 'p':
          p_tags_between_h3_h2.append(current_tag)
        current_tag = current_tag.find_next_sibling()
      for p_tag in p_tags_between_h3_h2:
        check_for_strong = p_tag.find('strong')
        if not check_for_strong:
          discription = discription+p_tag.get_text(strip=True)
    objectData['reviews'] = discription
    mainData.append(objectData)
  except:
    mainData.append({'Name':'','Telephone':'',"Email":'','Links':url})
    print("------------------------------Errrrrroooooorrrr")
    print('------------------------',url,'--------------------------')
  finally:
    print("The is finished",count)



# Specify the top-level directory where you want to search for Excel files
current_directory = os.getcwd()

# Use the glob module to search for Excel files (files with .xlsx or .xls extension)
excel_files = glob.glob(os.path.join(current_directory, "*.xls*"))

for excel_file in excel_files:
    file_name = os.path.basename(excel_file)
    sheet_name = 'Sheet1'
    df_read = pd.read_excel(file_name, sheet_name=sheet_name)
    print("------------------file-Name--------",file_name)
    df_read['Scraped Data'] = df_read['Links'].apply(scrape_data)
    df1 = pd.DataFrame(mainData)
    excel_file_path = f'final-list-fca-{file_name}.xlsx'
    df1.to_excel(excel_file_path, index=False)
    mainData = []  # Set index=False to exclude row numbers
    print(f"Excel file '{excel_file_path}' created successfully.")


# excel_file = 'links_chunk_1_40.xlsx'  # Replace with your file name
# sheet_name = 'Sheet1'  # Replace with your sheet name
# df_read = pd.read_excel(excel_file, sheet_name=sheet_name)
# df_read['Scraped Data'] = df_read['Links'].apply(scrape_data)

# df1 = pd.DataFrame(mainData)
# excel_file_path = 'final-list-fca.xlsx'
# df1.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
# print(f"Excel file '{excel_file_path}' created successfully.")

# https://www.fca.org.uk/news/warnings/brenner-and-associates
end_time = time.time()
execution_time_seconds = end_time - start_time
print("execution_time_seconds-------------",execution_time_seconds)
execution_time_minutes, execution_time_seconds = divmod(execution_time_seconds, 60)
execution_time_hours, execution_time_minutes = divmod(execution_time_minutes, 60)

print(f"Execution time: {int(execution_time_hours)} hours and {int(execution_time_minutes)} minutes")
