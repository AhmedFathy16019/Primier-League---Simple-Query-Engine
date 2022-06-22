import pandas as pd
import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Opening browser
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.maximize_window()
driver.implicitly_wait(5)
url = 'https://www.premierleague.com/results'
driver.get(url)

# Accept on Cookies
time.sleep(4)
accept_cookies = driver.find_element(By.XPATH, "//button[normalize-space()='Accept All Cookies']")
accept_cookies.click()

match_url = []

match_list = []
matches_list = []

for x in range(0, 4):
    # Choose Season
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(4)
    season_but = driver.find_element(By.XPATH, "//*[@id='mainContent']/div[3]/div[1]/section/div[3]/div[2]")
    season_but.click()
    time.sleep(4)
    season_but = driver.find_elements(By.XPATH, "//*[@id='mainContent']/div[3]/div[1]/section/div[3]/ul/li")
    season_but[x].click()

    # Scroll down
    current_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == current_height:
            break
        current_height = new_height

    time.sleep(4)
    matches = driver.find_elements(By.XPATH, "//*[@class = 'matchFixtureContainer']")
    time.sleep(4)

    for match in matches:
        match_home = match.find_element(By.XPATH, ".//div[1]/span[1]/span[1]/span[1]/span[1]/span[1]").text
        match_away = match.find_element(By.XPATH, ".//div[1]/span[1]/span[1]/span[3]/span[2]/span[1]").text
        match_result = match.find_element(By.XPATH, ".//div[1]/span[1]/span[1]/span[2]").text
        match_std = match.find_element(By.XPATH, ".//div[1]/span[1]/span[2]").get_attribute("textContent")
        match_season = driver.find_element(By.XPATH, "//*[@id='mainContent']/div[3]/div[1]/section/div[3]/div[2]").text
        match_date = match.find_element(By.XPATH, ".//../..").get_attribute("data-competition-matches-list")
        match_url = match.get_attribute("data-comp-match-item")

        matches_dict = {
            "stadium": match_std,
            "date": match_date,
            "season": match_season,
            "home": match_home,
            "away": match_away,
            "result": match_result
        }
        matches_list.append(matches_dict)

# Create a DataFrame and Export CSV
    df = pd.DataFrame(matches_list)
    df.to_csv(r'matches_Data.csv', index=True)

for url in match_url:
    try:
        driver.get('https://www.premierleague.com/match/' + url)
        time.sleep(2)
        stats = driver.find_element(By.XPATH, "//li[@role='tab'][normalize-space()='Stats']")
        stats.click()

        time.sleep(2)
        match_home = driver.find_element(By.CSS_SELECTOR, "div[class='team home'] span[class='long']").text
        match_away = driver.find_element(By.CSS_SELECTOR, "div[class='team away'] span[class='long']").text

        match_std = driver.find_element(By.XPATH, "//div[@class='stadium']").text
        match_date = driver.find_element(By.XPATH, "//div[@class='matchDate renderMatchDateContainer']").get_attribute("textContent")

        match_possession_h = driver.find_element(By.XPATH, "//p[normalize-space()='Possession %']/../../td[1]/p").text
        match_possession_aw = driver.find_element(By.XPATH, "//p[normalize-space()='Possession %']/../../td[3]/p").text

        match_goals_h = (driver.find_element(By.XPATH, "//div[@class='score fullTime']").text[0])
        match_goals_aw = (driver.find_element(By.XPATH, "//div[@class='score fullTime']").text[2])

        match_shots_h = driver.find_element(By.XPATH, "//p[normalize-space()='Shots']/../../td[1]/p").text
        match_shots_aw = driver.find_element(By.XPATH, "//p[normalize-space()='Shots']/../../td[3]/p").text

        match_fouls_h = driver.find_element(By.XPATH, "//p[normalize-space()='Fouls conceded']/../../td[1]/p").text
        match_fouls_aw = driver.find_element(By.XPATH, "//p[normalize-space()='Fouls conceded']/../../td[3]/p").text

        if len(driver.find_elements(By.XPATH, "//p[normalize-space()='Yellow cards']")) > 0:
            match_y_cards_h = driver.find_element(By.XPATH, "//p[normalize-space()='Yellow cards']/../../td[1]/p").text
            match_y_cards_aw = driver.find_element(By.XPATH, "//p[normalize-space()='Yellow cards']/../../td[3]/p").text
        else:
            match_y_cards_h = '0'
            match_y_cards_aw = '0'

        if len(driver.find_elements(By.XPATH, "//p[normalize-space()='Red cards']")) > 0:
            match_r_cards_h = driver.find_element(By.XPATH, "//p[normalize-space()='Red cards']/../../td[1]/p").text
            match_r_cards_aw = driver.find_element(By.XPATH, "//p[normalize-space()='Red cards']/../../td[3]/p").text
        else:
            match_r_cards_h = '0'
            match_r_cards_aw = '0'

        match_dict = {
            "home": match_home,
            "away": match_away,
            "stadium": match_std,
            "date": match_date,
            "goals_h:": match_goals_h,
            "goals_aw": match_goals_aw,
            "possession_h": match_possession_h,
            "possession_aw": match_possession_aw,
            "shots_h": match_shots_h,
            "shots_aw": match_shots_aw,
            "fouls_h": match_fouls_h,
            "fouls_aw": match_fouls_aw,
            "yellow_h": match_y_cards_h,
            "yellow_aw": match_y_cards_aw,
            "red_h": match_r_cards_h,
            "red_aw": match_r_cards_aw
        }
        match_list.append(match_dict)

    except selenium.common.exceptions.WebDriverException:
        print('Stopped')
        continue

# Create a DataFrame and Export CSV
    df = pd.DataFrame(match_list)
    df.to_csv(r'match_stats.csv', index=True)
