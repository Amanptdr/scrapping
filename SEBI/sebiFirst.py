import os
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
    response = requests.get("https://www.sebi.gov.in/sebi_data/attachdocs/oct-2023/1697457016091_1.pdf",stream = True)
    details = BeautifulSoup(response.text, 'html.parser')
    print(details.find(class_="immediate bottom_space"))
  except Exception as e:
    print("------------------",e,'--------------------')
    mainData.append({'company':'',"Disqualifications":'','Links':url})
    print("Something went wrong")
  finally:
    print("The 'try except' is finished")


def download_pdf_file(url: str) -> bool:
    response = requests.get(url, stream=True)
    pdf_file_name = os.path.basename(url)
    print(response,"responseresponseresponse")
    print(pdf_file_name,"responseresponseresponse")
    if response.status_code == 200:
        # Save in current working directory
        filepath = os.path.join(os.getcwd(), pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{pdf_file_name} was successfully saved!')
            return True
    else:
        print(f'Uh oh! Could not download {pdf_file_name},')
        print(f'HTTP response status code: {response.status_code}')
        return False
download_pdf_file("https://www.sebi.gov.in/sebi_data/attachdocs/oct-2023/1697457016091_1.pdf")





# if __name__ == '__main__':
#     # URL from which pdfs to be downloaded
#     URL ="https://www.sebi.gov.in/sebi_data/attachdocs/oct-2023/1697457016091_1.pdf"
#     download_pdf_file(URL)
