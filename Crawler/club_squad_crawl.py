import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Openning browser
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.maximize_window()
driver.implicitly_wait(30)
url = 'https://www.premierleague.com/clubs'
driver.get(url)

# Accepting Cookies
time.sleep(2)
accept_cookies = driver.find_element(By.XPATH, "//button[normalize-space()='Accept All Cookies']")
time.sleep(2)
accept_cookies.click()

# Get all clubs
clubs = driver.find_elements(By.XPATH, '//tbody/tr')

club_url = []
club_squad_list = []

for club in clubs:
    club_url.append(club.find_element(By.XPATH, ".//td[@class = 'team']/a").get_attribute("href"))

for ul in club_url:
    driver.get(ul.replace("overview", "squad"))
    squad_info = driver.find_elements(By.XPATH, "//*[@id='mainContent']/div[3]/div/ul/li")
    for sq in squad_info:
        club_name = driver.find_element(By.XPATH, "//div[@class='clubDetails']/h1").text
        club_player = sq.find_element(By.XPATH, ".//a/header/span/h4[@class = 'name']").text
        player_number = sq.find_element(By.XPATH, ".//a/header/span/span[@class = 'number']").text

        club_squad_dict = {
            "club": club_name,
            "player": club_player,
            "player_number": player_number
        }
        club_squad_list.append(club_squad_dict)

# Create a DataFrame and Export CSV
    df = pd.DataFrame(club_squad_list)
    df.to_csv(r'club_squad.csv', index=True)
