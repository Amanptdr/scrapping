import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

url = 'https://www.ice.gov/most-wanted'
response = requests.get(url)
driver = webdriver.Chrome()
driver.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    wanted_individuals = soup.find_all(class_='field-content')  # Replace with the actual class name
    most_wanted_data = []
    for individual in wanted_individuals:
        name = individual.find(class_='mw-name').text.strip()  # Replace with the actual class name
        photo_url = individual.find('img')['src']
        # mw-image
        most_wanted_data.append({
            'Name': name,
            'Photo_URL': photo_url,
        })
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
count = 1
def getWantedData(count):
  print(count)    
pageData = driver.find_element(By.XPATH, '//*[@id="blazy-views-most-wanted-block-block-1-1"]')
pageList = pageData.find_elements(By.TAG_NAME, 'li')
for item in pageList:
  itemXpath = driver.execute_script("return arguments[0].getAttribute('xpath')", item)
  try:
        wait.until(EC.element_to_be_clickable((By.XPATH, str(itemXpath))))
  except Exception as e:
    print(f"Error waiting for element: {e}")
  if item.is_enabled():
    item.click()
    sleep(10)
    getWantedData(count)
    count+=1
