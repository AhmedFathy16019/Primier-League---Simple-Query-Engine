import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Openning browser
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.maximize_window()
driver.implicitly_wait(5)
url = 'https://www.premierleague.com/clubs'
driver.get(url)

# Accepting Cookies
time.sleep(5)
accept_cookies = driver.find_element(By.XPATH, "//button[normalize-space()='Accept All Cookies']")
accept_cookies.click()

# Get all clubs
clubs = driver.find_elements(By.XPATH, '//*[@id="mainContent"]/div[2]/div/div/div[3]/div/table/tbody/tr')

# Get all urls for club overview
club_stadiums = []
stadiums_name = []
stadiums_address = []
stadiums_bd = []
stadiums_record_atd = []
stadiums_cap = []
stadiums_pitch_size = []

for club in clubs:
    stadiums_name.append(club.find_element(By.XPATH, "./td[2]/a").text)
    club_stadiums.append(club.find_element(By.XPATH, './td[2]/a').get_attribute("href"))

for club_stadium in club_stadiums:
    driver.get(club_stadium)
    stadium_info = driver.find_elements(By.XPATH, ".//li[normalize-space()='Stadium Information']")
    if len(stadium_info) > 0:
        stadium_info[0].click()
        stadiums_address.append(driver.find_element(By.XPATH, "//*[contains(text(), 'Stadium address')]/..").get_attribute("textContent").split(":")[1])
        if len(driver.find_elements(By.XPATH, ".//div[@class='articleTab active']/p/strong[contains(text(), 'pened')]/..")) > 0:
            stadiums_bd.append(driver.find_element(By.XPATH, ".//div[@class='articleTab active']/p/strong[contains(text(), 'pened')]/..").get_attribute("textContent").split(":")[1])
        else:
            if len(driver.find_elements(By.XPATH, ".//div[@class='articleTab active']/p/strong[contains(text(), 'uilt')]/..")) > 0:
                stadiums_bd.append(driver.find_element(By.XPATH, ".//div[@class='articleTab active']/p/strong[contains(text(), 'uilt')]/..").get_attribute("textContent").split(":")[1])
            else:
                stadiums_bd.append(None)
        if len(driver.find_elements(By.XPATH, ".//p[6]")) < 1:
            stadiums_record_atd.append(None)
        else:
            stadiums_record_atd.append(driver.find_elements(By.XPATH, ".//p[6]")[0].text)
        if len(driver.find_elements(By.XPATH, ".//div[@class='articleTab active']/p/strong[contains(text(), 'apacity')]/..")) > 0:
            stadiums_cap.append(driver.find_element(By.XPATH, ".//div[@class='articleTab active']/p/strong[contains(text(), 'apacity')]/..").get_attribute("textContent").split(":")[1])
        else:
            stadiums_cap.append(None)
        if len(driver.find_elements(By.XPATH, "//*[contains(text(), 'Pitch size')]/..")) > 0:
            stadiums_pitch_size.append(driver.find_element(By.XPATH, "//*[contains(text(), 'Pitch size')]/..").get_attribute("textContent").split(":")[1])
        else:
            stadiums_pitch_size.append(None)
    else:
        stadiums_bd.append(None)
        stadiums_record_atd.append(None)
        stadiums_cap.append(None)
        stadiums_pitch_size.append(None)

with open("stadiums.csv", "w", newline='') as file:
    output = csv.writer(file)
    for name, addr, bd, record, cap, size in zip(stadiums_name, stadiums_address, stadiums_bd, stadiums_record_atd, stadiums_cap, stadiums_pitch_size):
        output.writerow([name, addr, bd, record, cap, size])
