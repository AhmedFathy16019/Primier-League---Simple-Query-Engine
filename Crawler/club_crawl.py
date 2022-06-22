import time
import csv

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Openning browser
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
url = 'https://www.premierleague.com/clubs'
driver.get(url)

# Accepting Cookies
time.sleep(3)
accept_cookies = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()

# Get all clubs
clubs = driver.find_elements(By.XPATH, '//*[@id="mainContent"]/div[2]/div/div/div[3]/div/table/tbody/tr')

# Breaking down the club names and stadiums
club_names = []
club_stadiums = []
for club in clubs:
    club_names.append(club.find_element(By.XPATH, ".//td[@class='team']//h4[@class='clubName']").text)
    club_stadiums.append(club.find_element(By.XPATH, "./td[2]/a").text)

# Get all urls for club overview
clubs_overviews = []
clubs_website = []
for club in clubs:
    clubs_overviews.append(club.find_element(By.XPATH, './td[1]/a[1]').get_attribute("href"))

# Getting official websites for all clubs
for club_overviews in clubs_overviews:
    driver.get(club_overviews)
    # Handling Clubs that have no website
    try:
        clubs_website.append(driver.find_element(By.XPATH, ".//div[@class = 'website']/a").text)
    except selenium.common.exceptions.NoSuchElementException:
        clubs_website.append(None)

# Writing CSV File
with open("clubs.csv", "w", newline='') as file:
    output = csv.writer(file)
    for club_name, club_stadium, clubs_web in zip(club_names, club_stadiums, clubs_website):
        output.writerow([club_name, club_stadium, clubs_web])
