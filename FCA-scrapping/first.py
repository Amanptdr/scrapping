import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import pandas as pd
url = "https://www.fca.org.uk/views/ajax?_wrapper_format=drupal_ajax"
linkArr = []
for page in range(491):
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
    linkArr.append(link_element)
df = pd.DataFrame(linkArr, columns=['Links'])
excel_filename = 'linksFca1.xlsx'
df.to_excel(excel_filename, index=False)
print(df)