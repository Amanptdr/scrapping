import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
linkArr = []
mainData=[]

def scrape_data(url):
  objectData = {}
  try:
    response = requests.get(url)
    details = BeautifulSoup(response.text, 'html.parser')
    element = details.find(id=['section-clone-firm-details','section-unauthorised-firm-details'])
    heading = element.find_all('h2')
    objectData['heading'] = heading[0].text.strip()
    pTags = element.find_all('p')
    discription = ''
    for item in pTags:
      strong = item.find('strong')
      if strong:
        key = strong.text.strip()[:-1]
        value = strong.find_next_sibling(text=True).strip()
        objectData[key] = value
      else:
        child_tags = item.find_all()
        h2_tag = item.find_previous('h2')
        if not child_tags and not h2_tag:
          discription = discription+item.text.strip()
    objectData['reviews'] = discription
    objectData['Links'] = url
    mainData.append(objectData)
    print('------------------------',url,'--------------------------')
  except:
    mainData.append({'Name':'','Telephone':'',"Email":'','Links':url})
    print("Something went wrong")
  finally:
    print("The 'try except' is finished")
  time.sleep(1)


for page in range(491):
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
    linkArr.append(link_element)
    time.sleep(3)
df = pd.DataFrame(linkArr, columns=['Links'])
excel_filename = 'linksFcaNext.xlsx'
df.to_excel(excel_filename, index=False)


df1 = pd.DataFrame(mainData)
excel_file_path = 'mainDataNext.xlsx'
df1.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
print(f"Excel file '{excel_file_path}' created successfully.")




# https://www.fca.org.uk/news/warnings/brenner-and-associates