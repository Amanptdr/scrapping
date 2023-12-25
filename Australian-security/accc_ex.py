from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import requests
from io import StringIO
import os

count = 1
driver = webdriver.Chrome()
url = "https://www.accc.gov.au/public-registers/authorisations-and-notifications-registers/exclusive-dealing-notifications-register"
driver.get(url)
view_all = driver.find_element(By.XPATH, '//*[@id="block-acccgov-thememainpagecontent"]/article/div/div[6]/div/div/div/div[2]/a').click()
time.sleep(4)
last_page = driver.find_element(By.XPATH, '//*[@id="block-acccgov-thememainpagecontent"]/article/div/div/div/div/div/div[1]/nav/ul/li[12]/a')
last_page_num = last_page.get_attribute("href").split("=")[3]
all_data = []
time.sleep(4)
for i in range(int(last_page_num)+1):
    response = requests.get(f"https://www.accc.gov.au/public-registers/browse-public-registers?f%5B0%5D=type%3Aacccgov_notification&f%5B1%5D=acccgov_notification_type%3A510&page={i}")
    # print(f"https://www.accc.gov.au/public-registers/browse-public-registers?f%5B0%5D=type%3Aacccgov_notification&f%5B1%5D=acccgov_notification_type%3A510&page={i}")
    soup = BeautifulSoup(response.text, 'html.parser')
    main_div = soup.find("div",{"class":"accc-cards accc-cards--full_width"})
    count += 1
    # print(count)
    time.sleep(10)
    for i in main_div.find_all("div",{"class":"accc-card__inner"}):
        responses = requests.get("https://www.accc.gov.au"+i.find("a")["href"])
        soups = BeautifulSoup(responses.text, 'html.parser')
        company = soups.find("div",{"class":"block-page-title-block"}).text
        date_lodged = soups.find("div",{"class":"field--type-datetime"}).find("div",{"class":"field__item"}).text
        type = soups.find("div",{"class":"field--name-field-acccgov-notification-type"}).find("div",{"class":"field__item"}).text
        status = soups.find("div",{"class":"field--name-field-acccgov-pub-reg-status"}).find("div",{"class":"field__item"}).text
        try:
            outcome = soups.find("div",{"class":"field--name-field-acccgov-pub-reg-outcome"}).text
        except:
            outcome = ""
        applicants_data = soups.find("div",{"class":"field--name-field-acccgov-applicants"}).find("div",{"class":"field__items"}).text.strip().split("\n")
        applicants = ", ".join(applicants_data)
        notificaton_numbers = soups.find("div",{"class":"field--name-field-acccgov-notification-nums"}).find("div",{"class":"field__items"}).text.strip().split("\n")
        notificatons_numbers = ", ".join(notificaton_numbers)
        # print(notificatons_numbers)
        summary = soups.find("div",{"class":"field--name-field-accc-body"}).find("div",{"class":"field__item"}).text
        # table_data = soups.find("div",{"class":"block-system-main-block"}).find("table").find("tbody")
        # target_name = []
        # target_notification_number = []
        # target_date_lodged = []
        # for n in table_data.find_all("tr"):
        #     target_name.append(n.find_all("td")[0].text)
        #     target_notification_number.append(n.find_all("td")[1].text)
        #     target_date_lodged.append(n.find_all("td")[2].text.strip())
        # target_names = ", ".join(target_name)
        # target_notification_numbers = ", ".join(target_notification_number)
        # target_dates_lodged = ", ".join(target_date_lodged)
        
        # target = soups.find("div",{"class":"field--name-field-acccgov-pub-reg-targets"}).text.strip().split("\n")
        # target_data = []
        # for m in target:
        #     if len(m.strip()) != 0:
        #         target_data.append(m)
        div_data = soups.find("div",{"class":"view-acccgov-public-register-documents"})
        decisions_date = ""
        decisions_links = ""
        accc_correspondence_links = ""
        accc_correspondence_date = ""
        submissions_link = ""
        submissions_date = ""
        consultations_links = ""
        consultations_date = ""
        pre_decision_link = ""
        pre_decision_date = "" 
        time.sleep(5)
        for k in div_data.find_all("div",{"class":"view-grouping"}):
            other_detail_arr = k.text.split("\n")
            cleaned_list = [item.replace('\n', ',') for item in other_detail_arr]
            aaa = []
            bbb = []
            for j in cleaned_list:
                if len(j.strip()) != 0:
                    bbb.append(j)
            print(bbb)
            if bbb[0] == "Notifications":
                link_arr = []
                for l in k.find_all("a"):
                    if l["href"] not in link_arr:
                        if len(l["href"]) != 0:
                            link_arr.append("https://www.accc.gov.au" + l["href"])
                notifications_links_array = list(set(link_arr))
                notifications_links = " ,".join(notifications_links_array)
                date_arr = []
                for p in bbb:
                    if "PDF" in p:
                        try:
                            date_arr.append(bbb[bbb.index(p)+1])
                        except:
                            pass
                notifications_date = ", ".join(date_arr)
            if bbb[0] == "Decisions":
                link_arr = []
                for l in k.find_all("a"):
                    if l["href"] not in link_arr:
                        if len(l["href"]) != 0:
                            link_arr.append("https://www.accc.gov.au" + l["href"])
                decisions_links_array = list(set(link_arr))
                decisions_links = " ,".join(decisions_links_array)
                date_arr = []
                for p in bbb:
                    if "PDF" in p:
                        # print("122",bbb)
                        try:
                            date_arr.append(bbb[bbb.index(p)+1])
                        except:
                            pass
                decisions_date = ", ".join(date_arr)
            if bbb[0] == "Consultations":
                link_arr = []
                for l in k.find_all("a"):
                    if l["href"] not in link_arr:
                        if len(l["href"]) != 0:
                            link_arr.append("https://www.accc.gov.au" + l["href"])
                consultations_links_array = list(set(link_arr))
                consultations_links = " ,".join(consultations_links_array)
                date_arr = []
                for p in bbb:
                    if "PDF" in p:
                        date_arr.append(bbb[bbb.index(p)+1])
                consultations_date = ", ".join(date_arr)
            if bbb[0] == "ACCC correspondence":
                link_arr = []
                for l in k.find_all("a"):
                    if l["href"] not in link_arr:
                        if len(l["href"]) != 0:
                            link_arr.append("https://www.accc.gov.au" + l["href"])
                accc_correspondence_links_array = list(set(link_arr))
                accc_correspondence_links = " ,".join(accc_correspondence_links_array)
                date_arr = []
                for p in bbb:
                    if "PDF" in p:
                        try:
                            # print(bbb)
                            # print(bbb[bbb.index(p)+1])
                            date_arr.append(bbb[bbb.index(p)+1])
                        except:
                            pass
                accc_correspondence_date = ", ".join(date_arr)
            if bbb[0] == "Submissions":
                submissions_links_arr = []
                for l in k.find_all("a"):
                    if l["href"] not in submissions_links_arr:
                        if len(l["href"]) != 0:
                            submissions_links_arr.append("https://www.accc.gov.au" + l["href"])
                submissions_links_array = list(set(submissions_links_arr))
                submissions_links = " ,".join(submissions_links_array)
                submissions_link = submissions_links
                date_arr = []
                for p in bbb:
                    if "PDF" in p:
                        date_arr.append(bbb[bbb.index(p)+1])
                submissions_date = ", ".join(date_arr)
            if bbb[0] == "Pre-decision conferences":
                # print(bbb)
                pre_decision_links_arr = []
                for l in k.find_all("a"):
                    if l["href"] not in pre_decision_links_arr:
                        if len(l["href"]) != 0:
                            pre_decision_links_arr.append("https://www.accc.gov.au" + l["href"])
                pre_decision_links_array = list(set(pre_decision_links_arr))
                pre_decision_links = " ,".join(pre_decision_links_array)
                pre_decision_link = pre_decision_links
                date_arr = []
                for p in bbb:
                    if "PDF" in p:
                        date_arr.append(bbb[bbb.index(p)+1])
                pre_decision_date = ", ".join(date_arr)
        # break
        data = {
            "Company Name":company.strip(),
            "Date lodged":date_lodged.strip(),
            "Type":type,
            "Status":status,
            "Outcome":outcome,
            "Applicant(s)":applicants,
            "Notification number(s)":notificatons_numbers,
            # "Lodged on behalf of":lodged_on_behalf_of_array_final,
            "Summary":summary.strip(),
            # "Target":target_names,
            # "Target Notification Numbers":target_notification_numbers,
            # "Target Date lodged":target_dates_lodged,
            "Notifications Document Link":notifications_links,
            "Notifications Document Date":notifications_date,
            "Decisions Document Link":decisions_links,
            "Decisions Document Date":decisions_date,
            "Consultations Document Link":consultations_links,
            "Consultations Document Date":consultations_date,
            "ACCC correspondence Document Link":accc_correspondence_links,
            "ACCC correspondence Document Date":accc_correspondence_date,
            "Submissions Document Link":submissions_link,
            "Submissions Document Date":submissions_date,
            "Pre-decision conferences Document Link":pre_decision_link,
            "Pre-decision conferences Document Date":pre_decision_date,
        }
        all_data.append(data)
        # break
driver.quit()
df = pd.DataFrame(all_data)
df.to_excel("accc_exclusive_dealing_notification_register1.xlsx", index = False)
        