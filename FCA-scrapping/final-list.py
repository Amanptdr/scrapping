import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
import time
from urllib.parse import urlparse, parse_qs

start_time = time.time()

linkArr = []
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

url = "https://www.fca.org.uk/views/ajax?_wrapper_format=drupal_ajax"
chunk_size = 1000
all_links = []
fileName = 1
payload = {'view_name': 'component_warnings_glossary',
    'view_display_id': 'component_warnings_glossary_block',
    'view_args': '',
    'view_path': '/node/3361',
    'view_base_path': '',
    'view_dom_id': 'b355593918cb2cd9e1b89195608838c6f7beba11eb09de8ba665e572a76c0f8a',
    'pager_element': '0',
    'page': 0,
    '_drupal_ajax': '1',
    'ajax_page_state[theme]': 'fca',
    'ajax_page_state[theme_token]': '',
    'ajax_page_state[libraries]': 'blazy/bio.ajax,bootstrap/popover,ckeditor_indentblock/indentblock,core/drupal.autocomplete,eu_cookie_compliance/eu_cookie_compliance_default,extlink/drupal.extlink,facets/drupal.facets.views-ajax,fca/4_column_content,fca/copy_highlighted,fca/fca_colours,fca/fca_funnelback_search_form,fca/global-styling,fca/glossary,fca/page_feedback_form,fca/read_next_previous,fca/social,fca/theme.scrollspy,fca_cookie_compliance/fca_cookie_compliance,fca_cookie_compliance/fca_cookie_compliance_gtm,fca_funnelback/funnelback-autocomplete,fca_popup/popup-banner,fca_webforms/metatags,paragraphs/drupal.paragraphs.unpublished,poll/drupal.poll-links,printable/entity-links,search_api_autocomplete/search_api_autocomplete,selection_sharer/selection-shared,system/base,views/views.ajax,views/views.module,webform/webform.composite,webform/webform.element.details.save,webform/webform.element.details.toggle,webform/webform.element.message,webform/webform.element.options,webform/webform.form'}
files=[]
res_pagination = requests.request("POST", url, headers='', data=payload, files=files)
json_object_pagination = json.loads(res_pagination.text)
pageData_pagination = BeautifulSoup(json_object_pagination[2]['data'], 'html.parser')
parse_result = urlparse(pageData_pagination.find('li',class_="pager__item--last").find('a').get("href"))
total_pages = int(parse_qs(parse_result.query)['page'][0])
print(total_pages)
for page in range(total_pages+1):
  # url = "https://www.fca.org.uk/views/ajax?_wrapper_format=drupal_ajax"
  url = f"https://www.fca.org.uk/views/ajax?_wrapper_format=drupal_ajax&view_name=component_warnings_glossary&view_display_id=component_warnings_glossary_block&view_args=&view_path=%2Fnode%2F3361&view_base_path=&view_dom_id=427796d83499b588e61c0e1602d903b8b8d0a189e4b4c26f59df0625323cc607&pager_element=0&page={page}&_drupal_ajax=1&ajax_page_state%5Btheme%5D=fca&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=blazy%2Fbio.ajax%2Cbootstrap%2Fpopover%2Cckeditor_indentblock%2Findentblock%2Ccore%2Fdrupal.autocomplete%2Ceu_cookie_compliance%2Feu_cookie_compliance_default%2Cextlink%2Fdrupal.extlink%2Cfacets%2Fdrupal.facets.views-ajax%2Cfca%2F4_column_content%2Cfca%2Fcopy_highlighted%2Cfca%2Ffca_colours%2Cfca%2Ffca_funnelback_search_form%2Cfca%2Fglobal-styling%2Cfca%2Fglossary%2Cfca%2Fpage_feedback_form%2Cfca%2Fread_next_previous%2Cfca%2Fsocial%2Cfca%2Ftheme.scrollspy%2Cfca_cookie_compliance%2Ffca_cookie_compliance%2Cfca_cookie_compliance%2Ffca_cookie_compliance_gtm%2Cfca_funnelback%2Ffunnelback-autocomplete%2Cfca_popup%2Fpopup-banner%2Cfca_webforms%2Fmetatags%2Cparagraphs%2Fdrupal.paragraphs.unpublished%2Cpoll%2Fdrupal.poll-links%2Cprintable%2Fentity-links%2Csearch_api_autocomplete%2Fsearch_api_autocomplete%2Cselection_sharer%2Fselection-shared%2Csystem%2Fbase%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module%2Cwebform%2Fwebform.composite%2Cwebform%2Fwebform.element.details.save%2Cwebform%2Fwebform.element.details.toggle%2Cwebform%2Fwebform.element.message%2Cwebform%2Fwebform.element.options%2Cwebform%2Fwebform.form"
  payload = {
    'view_name': 'component_warnings_glossary',
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
  # response = requests.request("POST", url, headers='', data=payload, files=files)
  response =requests.get(url)
  json_object = json.loads(response.text)
  pageData = BeautifulSoup(json_object[2]['data'], 'html.parser')
  tbody = pageData.find('tbody')
  print('------------------------',page,'------------------------------')
  for td in tbody.find_all(class_="views-field views-field-letter"):
    link_element = 'https://www.fca.org.uk'+td.find('a').get('href')
    linkArr.append(link_element)
df = pd.DataFrame(linkArr, columns=['Links'])
excel_filename = 'links.xlsx'
df.to_excel(excel_filename, index=False)
time.sleep(5)

excel_file = 'links.xlsx'  # Replace with your file name
sheet_name = 'Sheet1'  # Replace with your sheet name
df_read = pd.read_excel(excel_file, sheet_name=sheet_name)
df_read['Scraped Data'] = df_read['Links'].apply(scrape_data)

df1 = pd.DataFrame(mainData)
excel_file_path = 'data.xlsx'
df1.to_excel(excel_file_path, index=False)  # Set index=False to exclude row numbers
print(f"Excel file '{excel_file_path}' created successfully.")

end_time = time.time()
execution_time_seconds = end_time - start_time
print("execution_time_seconds-------------",execution_time_seconds)
execution_time_minutes, execution_time_seconds = divmod(execution_time_seconds, 60)
execution_time_hours, execution_time_minutes = divmod(execution_time_minutes, 60)

print(f"Execution time: {int(execution_time_hours)} hours and {int(execution_time_minutes)} minutes")
