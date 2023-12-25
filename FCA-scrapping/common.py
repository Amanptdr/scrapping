import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
import time
start_time = time.time()



linkArr = []
mainData=[]

def decode_email(encoded_email):
  try:
    r = int(encoded_email[:2], 16)
    decoded_email = ''.join(
      [chr(int(encoded_email[i:i+2], 16) ^ r) for i in range(2, len(encoded_email), 2)]
      )
  except:
    decoded_email = ""
  return decoded_email
def scrape_data(url):
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
          decoded_email = decode_email(item.find('a').get('data-cfemail'))
          value = decoded_email
        objectData[key] = value
      else:
        # child_tags = item.find_all()
        # h2_tag = item.find_previous('h2')
        # print(h2_tag)
        # if not child_tags and not h2_tag:
        # if not h2_tag:
        if not find_by_class:
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
    # objectData['Links'] = url
    mainData.append(objectData)
    print('------------------------',url,'--------------------------')
  except:
    mainData.append({'Name':'','Telephone':'',"Email":'','Links':url})
    print("------------------------------Errrrrroooooorrrr")
  finally:
    print("The is finished")
  # time.sleep(1)


for page in range(497):
  url = "https://www.fca.org.uk/views/ajax?_wrapper_format=drupal_ajax"
  payload = {'view_name': 'component_warnings_glossary',
  'view_display_id': 'component_warnings_glossary_block',
  'view_args': '',
  'view_path': '/node/3361',
  'view_base_path': '',
  'view_dom_id': 'b355593918cb2cd9e1b89195608838c6f7beba11eb09de8ba665e572a76c0f8a',
  'pager_element': '0',
  'page': page,
  '_drupal_ajax': '1',
  'ajax_page_state[theme]': 'fca',
  'ajax_page_state[theme_token]': '',
  'ajax_page_state[libraries]': 'blazy/bio.ajax,bootstrap/popover,ckeditor_indentblock/indentblock,core/drupal.autocomplete,eu_cookie_compliance/eu_cookie_compliance_default,extlink/drupal.extlink,facets/drupal.facets.views-ajax,fca/4_column_content,fca/copy_highlighted,fca/fca_colours,fca/fca_funnelback_search_form,fca/global-styling,fca/glossary,fca/page_feedback_form,fca/read_next_previous,fca/social,fca/theme.scrollspy,fca_cookie_compliance/fca_cookie_compliance,fca_cookie_compliance/fca_cookie_compliance_gtm,fca_funnelback/funnelback-autocomplete,fca_popup/popup-banner,fca_webforms/metatags,paragraphs/drupal.paragraphs.unpublished,poll/drupal.poll-links,printable/entity-links,search_api_autocomplete/search_api_autocomplete,selection_sharer/selection-shared,system/base,views/views.ajax,views/views.module,webform/webform.composite,webform/webform.element.details.save,webform/webform.element.details.toggle,webform/webform.element.message,webform/webform.element.options,webform/webform.form'}
  files=[]
  response = requests.request("POST", url, headers='', data=payload, files=files)
  json_object = json.loads(response.text)
  pageData = BeautifulSoup(json_object[2]['data'], 'html.parser')
  tbody = pageData.find('tbody')
  print('------------------------',page,'------------------------------')
  for td in tbody.find_all(class_="views-field views-field-letter"):
    link_element = 'https://www.fca.org.uk'+td.find('a').get('href')
    scrape_data(link_element)
    # linkArr.append(link_element)
    # time.sleep(3)
# df = pd.DataFrame(linkArr, columns=['Links'])
# excel_filename = 'linksFcaNext.xlsx'
# df.to_excel(excel_filename, index=False)


df1 = pd.DataFrame(mainData)
excel_file_path = '1/11/2023-fca1.xlsx'
df1.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
print(f"Excel file '{excel_file_path}' created successfully.")

end_time = time.time()
execution_time_seconds = end_time - start_time
print("execution_time_seconds-------------",execution_time_seconds)
execution_time_minutes, execution_time_seconds = divmod(execution_time_seconds, 60)
execution_time_hours, execution_time_minutes = divmod(execution_time_minutes, 60)

print(f"Execution time: {int(execution_time_hours)} hours and {int(execution_time_minutes)} minutes")



# https://www.fca.org.uk/news/warnings/brenner-and-associates