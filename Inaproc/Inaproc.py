from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
data_List = []
driver = webdriver.Chrome()
url = "https://inaproc.id/daftar-hitam"
driver.get(url)
# time.sleep(30)

checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ctp-checkbox-label"))
          )
                
print("checkbox=",checkbox,"------")
checkbox.click()
time.sleep(20)
print("4564546546")
# print(driver.find_elements(By.XPATH,'//*[@id="blacklist"]/div[2]/div/section/div[3]/div[1]/table/tbody/tr[2]/td[1]/h5/a'))

# header = {
#   "Cookie":'_ga=GA1.2.1246711828.1699514530; _gid=GA1.2.1399896176.1699514530; cf_clearance=sk5neRa_oH_tCEKSbvLKI3WfBJUWFQ1tQinJq4fzSug-1699529281-0-1-39cf5504.a0d49c16.6ece0ae4-160.0.0; _gat=1; XSRF-TOKEN=eyJpdiI6ImtkcXJGaXVQaVhFNytVcCtFVE9Hc2c9PSIsInZhbHVlIjoiQmZpbW1iWXBhb21BZjRRUnVIYjZvVmpQQjRZWld5OXo0Y0l2XC85RGVZMG1PQzA0OWZSdGtobytZWFdlaUZrSkFESnhPWWQwVTVnUmtTVVRNVFBRdThnPT0iLCJtYWMiOiI4NzQ4MzRjYjVlYTMxNzhlZjBhZjQxZWE2OGJlODBlOTY3NDc5MGJkNWVkYWJhODMxMGNjZTZlZWE3NWQzNWI2In0%3D; laravel_session=eyJpdiI6IjRhdnREZGg0bkFhdnBiSmx2UkhwZkE9PSIsInZhbHVlIjoia0I1QjlsWlwvUG92akhEZnJabWkzSFhtd0l4Zys2V2t2XC8rR3NodzdrS21pUWpVbTJEWURSMng4TkNWQ3NwVkNET2EwemFHYXpaclpXSzhlZ3pQQ1UyUT09IiwibWFjIjoiZWYwOWEzZjRlM2I2MmYzODdlODM0YjE1MWFjMzdhMWNlMDRlNWY4YjYxNTIxYTUyNThjNzU4YzViYzRkYTZjMiJ9; _ga_88R0FJ6JMY=GS1.2.1699529289.2.1.1699529299.50.0.0',
#   "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
# }
# response = requests.request("GET", url, headers=header, data={})
# soup = BeautifulSoup(response.text,'html.parser')
# print(len(soup.find_all("table")))
# link_list = []

