# import requests
# from bs4 import BeautifulSoup
# from time import sleep
# import pandas as pd
# import json
# mainData=[]
# def decode_email(encoded_email):
#   try:
#     r = int(encoded_email[:2], 16)
#     decoded_email = ''.join(
#       [chr(int(encoded_email[i:i+2], 16) ^ r) for i in range(2, len(encoded_email), 2)]
#       )
#   except:
#     decoded_email = ""
#   return decoded_email
# def scrape_data(url):
#   objectData = {}
#   find_by_class = False
#   try:
#     response = requests.get(url)
#     details = BeautifulSoup(response.text, 'html.parser')
#     element = details.find(id=['section-clone-firm-details','section-unauthorised-firm-details'])
#     if element == None:
#       element = details.find(class_="copy-block default")
#       find_by_class = True
#     heading = element.find_all(['h2','h3'])
#     objectData['heading'] = heading[0].text.strip()
#     pTags = element.find_all('p')
#     discription = ''
#     for item in pTags:
#       strong = item.find('strong')
#       if strong:
#         key = strong.text.strip()[:-1]
#         if key!='Email':
#           value = strong.find_next_sibling(text=True).strip()
#         else:
#           decoded_email = decode_email(item.find('a').get('data-cfemail'))
#           value = decoded_email
#         objectData[key] = value
#       else:
#         if not find_by_class:
#           discription = discription+item.text.strip()
#         else:discription = ""
#     print(discription,"1-1-1-1-1-1") 
#     if find_by_class:
#       h3_tag = element.find('h3')
#       h2_tag = element.find('h2')
#       p_tags_between_h3_h2 = []
#       current_tag = h3_tag.find_next_sibling()
#       while current_tag and current_tag.name != 'h2':
#         if current_tag.name == 'p':
#           p_tags_between_h3_h2.append(current_tag)
#         current_tag = current_tag.find_next_sibling()
#       for p_tag in p_tags_between_h3_h2:
#         check_for_strong = p_tag.find('strong')
#         if not check_for_strong:
#           discription = discription+p_tag.get_text(strip=True)
#     objectData['reviews'] = discription
#     # objectData['Links'] = url
#     mainData.append(objectData)
#   except Exception as e:
#     mainData.append({'Name':'','Telephone':'',"Email":'','Links':url})
#     print("------------------------------Errrrrroooooorrrr",e)
#     print('------------------------',url,'--------------------------')
#   finally:
#     print("The is finished")



# # excel_file = 'linksFca1.xlsx'  # Replace with your file name
# # sheet_name = 'Sheet1'  # Replace with your sheet name
# # df1 = pd.read_excel(excel_file, sheet_name=sheet_name)
# # df1['Scraped Data'] = df1['Links'].apply(scrape_data)
# # scrape_data("https://www.fca.org.uk/news/warnings/pheno-fx")
# # https://www.fca.org.uk/news/warnings/diamond-futurity-fund-dff-ireland-limited-clone-fca-authorised-fund
# # https://www.fca.org.uk/news/warnings/prudential-clone-fca-recognised-products-and-uk-registered-company
# # https://www.fca.org.uk/news/warnings/garraway-bonds-clone-authorised-schedule-5-firm
# # https://www.fca.org.uk/news/warnings/fixed-term-market
# scrape_data("https://www.fca.org.uk/news/warnings/diamond-futurity-fund-dff-ireland-limited-clone-fca-authorised-fund")

# print(mainData)
# # df = pd.DataFrame(mainData)
# # excel_file_path = 'mainData.xlsx'
# # df.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
# # print(f"Excel file '{excel_file_path}' created successfully.")

from bs4 import BeautifulSoup

# Example HTML data
html_data = """
<p>Some text without anchor.</p>
<p>Some text with an anchor: <a class="abcd" href="example.com">Link</a></p>
<p>Another paragraph with an anchor: <a class="abcd" href="example.com">Link</a></p>
<p>Some more text without anchor.</p>
"""

# Create a BeautifulSoup object
soup = BeautifulSoup(html_data, 'html.parser')

# Find and remove <p> tags containing <a> tags with class "abcd"
for p_tag in soup.find_all('p'):
    a_tags = p_tag.find_all('a', class_='abcd')
    print(p_tag)
    if a_tags:
        p_tag.extract()

# Get the modified HTML data
modified_html = str(soup)

# Print the modified HTML data
print(modified_html)
