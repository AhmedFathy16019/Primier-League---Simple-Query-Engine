import pandas as pd
import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Opening browser
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.implicitly_wait(5)
driver.maximize_window()
url = 'https://www.premierleague.com/players'
driver.get(url)

# Accepting Cookies
time.sleep(4)
accept_cookies = driver.find_element(By.XPATH, "//button[normalize-space()='Accept All Cookies']")
accept_cookies.click()

# Get all urls for club overview

player_url = []
player_list = []
hist_list = []

for x in range(0, 4):
    # Choose Season
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    season_but = driver.find_element(By.XPATH, "//div[@data-dropdown-current='compSeasons']")
    season_but.click()
    time.sleep(2)
    season_but = driver.find_elements(By.XPATH, "//ul[@data-dropdown-list='compSeasons']/li")
    season_but[x].click()
    # Scroll down
    current_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == current_height:
            break
        current_height = new_height
    time.sleep(4)
    # Get all players
    players_names = driver.find_elements(By.XPATH, "//tbody/tr/td/a")
    for name in players_names:
        player_url.append(name.get_attribute("href"))

for url in player_url:
    try:
        driver.get(url)
        time.sleep(3)
        player_name = driver.find_element(By.XPATH, "//div[@class='playerDetails']//h1/div").text
        player_nationality = driver.find_element(By.XPATH, "//span[@class='playerCountry']").text
        player_position = driver.find_element(By.XPATH, "//*[@id='mainContent']/div[3]/nav/div/section[1]/div[text() = 'Position']/following-sibling::div").text
        if len(driver.find_elements(By.XPATH, "//div[normalize-space()='Date of Birth']/../div[2]")) > 0:
            player_dob = driver.find_element(By.XPATH, "//div[normalize-space()='Date of Birth']/../div[2]").text.split(' ')[0]
        else:
            player_dob = '_'
        if len(driver.find_elements(By.XPATH, "//ul[@class = 'pdcol3']/li[1]/div[2]")) > 0:
            player_height = driver.find_element(By.XPATH, "//ul[@class = 'pdcol3']/li[1]/div[2]").text
        else:
            player_height = '_'
        if len(driver.find_elements(By.XPATH, "//td[@class='team'][1]/a/span[2]")) > 0:
            player_club_cur = driver.find_element(By.XPATH, "//td[@class='team'][1]/a/span[2]").text
        else:
            player_club_cur = ''
        player_dict = {
            "name": player_name,
            "current club": player_club_cur,
            "nationality": player_nationality,
            "date of birth": player_dob,
            "position": player_position,
            "height": player_height,
        }
        player_list.append(player_dict)
        hist = driver.find_elements(By.XPATH, "//tbody/tr[@class = 'table']")
        for cl_hist in hist:
            player_club_hist = cl_hist.find_element(By.XPATH, ".//td[@class = 'team']/a/span[2]").text
            player_season = cl_hist.find_element(By.XPATH, ".//td[@class = 'season']/p").text
            hist_dict = {
                "name": player_name,
                "date of birth": player_dob,
                "club": player_club_hist,
                "season": player_season
            }
            hist_list.append(hist_dict)
    except selenium.common.exceptions.WebDriverException:
        print('Stopped')
        continue

# Create a DataFrame and Export CSV
df = pd.DataFrame(hist_list)
df.to_csv(r'Players_hist.csv', index=True)

# Create a DataFrame and Export CSV
df = pd.DataFrame(player_list)
df.to_csv(r'Players_List.csv', index=True)
