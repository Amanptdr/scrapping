import pandas as pd
from bs4 import BeautifulSoup
import requests
from googletrans import Translator
translator = Translator()

# Load the Excel file
excel_file = 'links50_100.xlsx'  # Replace with your file name
sheet_name = 'Sheet2'  # Replace with your sheet name
df = pd.read_excel(excel_file, sheet_name=sheet_name)
table_data = []
table_headers = []

def getHeaderData():
    print('header dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    res = requests.get('http://vpcqcsdt.bocongan.gov.vn/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3/ctl/chitiet/mid/1088/ma/d8240214-eef2-4c58-8202-99387fe818cd?returnUrl=/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3')
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find("table")
    one_row_data = []
    for row in table.find_all('tr'):
        for th in row.find_all('th'):
            text_to_translate = th.text.strip()
            try:
                translated_text = translator.translate(text_to_translate, src='vi', dest='en')
                table_headers.append(translated_text.text)
            except:
                table_headers.append(text_to_translate)
getHeaderData()

def scrape_data(link):
    print("start Third Step ----------33333333333333333333333333333333333",link)
    res = requests.get(link)
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find("table")
    one_row_data = []
    for row in table.find_all('tr'):
        total = len(row.find_all('th'))
        for td in row.find_all('td'):
            if total>0:
                if 'noborder' in td.get('class', []):
                    total = total-1
                    continue
                text_to_translate = td.text.strip()
                try:
                    translated_text = translator.translate(text_to_translate, src='vi', dest='en')
                    one_row_data.append(translated_text.text)
                except:
                    one_row_data.append(text_to_translate)
                total = total-1
    table_data.append(one_row_data)


df['Scraped Data'] = df['Links'].apply(scrape_data)  # Replace 'URL Column' with your column name
df = pd.DataFrame(table_data, columns=table_headers)
excel_filename = 'web_scraped_page_51_75.xlsx'
df.to_excel(excel_filename, index=False)
