import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from urllib.parse import urlparse, parse_qs

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
for page in range(total_pages+1):
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
    tds = pageData.find('tbody').find_all('td',class_='views-field views-field-letter')
    for td in tds:
      all_links.append('https://www.fca.org.uk'+td.find('a').get('href'))
    if len(all_links) >= chunk_size or page == total_pages:
      # Create a DataFrame from the links
      df = pd.DataFrame(all_links, columns=["Links"])
      # Save to an Excel file with a unique name based on the page number
      name = str(fileName)+"_"+str(page+1)
      file_name = f"links_chunk_{name}.xlsx"
      df.to_excel(file_name, index=False)
      all_links = []
      fileName = page+1
      print("-------",page,"----------")
    if page==total_pages:
      break