import pandas as pd
from bs4 import BeautifulSoup
import requests

# Load the Excel file
excel_file = 'links.xlsx'  # Replace with your file name
sheet_name = 'Sheet2'  # Replace with your sheet name
df = pd.read_excel(excel_file, sheet_name=sheet_name)
table_data = []
table_headers = []

def getHeaderData():
    res = requests.get('http://vpcqcsdt.bocongan.gov.vn/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3/ctl/chitiet/mid/1088/ma/d8240214-eef2-4c58-8202-99387fe818cd?returnUrl=/Truy-n%C3%A3-TP/%C4%90%E1%BB%91i-t%C6%B0%E1%BB%A3ng-truy-n%C3%A3')
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find("table")
    one_row_data = []
    for row in table.find_all('tr'):
        for th in row.find_all('th'):
            table_headers.append(th.text.strip())
getHeaderData()


def scrape_data(link):
    try:
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
                    one_row_data.append(td.text.strip())
                    total = total-1
        table_data.append(one_row_data)
    except:print('1111111111111111')

# Create a new column to store the scraped data
df['Scraped Data'] = df['Links'].apply(scrape_data)  # Replace 'URL Column' with your column name

# Save the updated DataFrame to a new Excel file
df = pd.DataFrame(table_data, columns=table_headers)
excel_filename = 'web_scraped_page_1_25.xlsx'
df.to_excel(excel_filename, index=False)
