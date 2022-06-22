import time
import MySQLdb as db
import os

HOST = "db4free.net"
USER = "ahmedfathy16019"
PASSWORD = "msiii_php"
DB = "csce2501_project"
connection = db.Connection(host=HOST, user=USER, passwd=PASSWORD, db=DB)
dbhandler = connection.cursor()
global user
global guest


def home_function():
    os.system('cls')
    print("Choose one of the following three options: "
          "\n 1. Login \n 2. Register New User \n 3. Use Guest Mode \n 4. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        login_function()
    elif choice == '2':
        register_function()
    elif choice == '3':
        guest_mode()
    elif choice == '4':
        exit_q()
    else:
        inv_in()


def login_function():
    os.system('cls')
    email = input('Enter your email: ')
    password = input('Enter your password: ')
    dbhandler.execute(f"SELECT * FROM fan WHERE fan_email = '{email}' AND fan_password = '{password}'")
    result = dbhandler.fetchall()
    if len(result):
        os.system('cls')
        print("Login Successful")
        time.sleep(1)
        user_queries()
    else:
        os.system('cls')
        print("Login Failed Choose: \n 1. Retry \n 2.Register \n 3. Use Guest Mode")
        login_choice = input("Enter Your Choice: ")
        if login_choice == '1':
            login_function()
        elif login_choice == '2':
            register_function()
        elif login_choice == '3':
            guest_mode()
        else:
            inv_in()


def user_queries():
    global user
    global guest
    user = 1
    guest = 0
    os.system('cls')
    print("Choose on of the following Queries: "
          "\n 1. Add a new user review on a match"
          "\n 2. View existing reviews on a given match "
          "\n 3. Register a user"
          "\n 4. Show all the players from a certain nationality and their home teams history "
          "\n 5. Show the top 10 teams by matches won, home matches won, yellow cards, fouls,and shots "
          "\n 6. Show all the teams who won the most games by season "
          "\n 7. Query and view a given team information"
          "\n 8. Query and view a given player information by full name"
          "\n 9. Identify the home team for a given stadium name"
          "\n 10. Show all the players who played a certain position"
          "\n 11. Identify all the teams in a given city in the UK"
          "\n 12. Exit")
    query = input("Enter your Choice: ")
    if query == '1':
        add_rev()
    elif query == '2':
        view_rev()
    elif query == '3':
        register_function()
    elif query == '4':
        pl_nat()
    elif query == '5':
        top_team()
    elif query == '6':
        top_team_season()
    elif query == '7':
        team_view()
    elif query == '8':
        pl_view()
    elif query == '9':
        home_std()
    elif query == '10':
        pl_pos()
    elif query == '11':
        city()
    elif query == '12':
        exit_q()
    else:
        inv_in()


def guest_mode():
    global user
    global guest
    user = 0
    guest = 1
    os.system('cls')
    print("Choose on of the following Operations: "
          "\n 1. View existing reviews on a given match"
          "\n 2. Register a user"
          "\n 3. Show all the players from a certain nationality and their home teams history "
          "\n 4. Show the top 10 teams by matches won, home matches won, yellow cards, fouls,and shots "
          "\n 5. Show all the teams who won the most games by season "
          "\n 6. Query and view a given team information"
          "\n 7. Query and view a given player information by full name"
          "\n 8. Identify the home team for a given stadium name"
          "\n 9. Show all the players who played a certain position"
          "\n 10. Identify all the teams in a given city in the UK"
          "\n 11. Exit")
    query = input("Enter your Choice: ")
    if query == '1':
        view_rev()
    elif query == '2':
        register_function()
    elif query == '3':
        pl_nat()
    elif query == '4':
        top_team()
    elif query == '5':
        top_team_season()
    elif query == '6':
        team_view()
    elif query == '7':
        pl_view()
    elif query == '8':
        home_std()
    elif query == '9':
        pl_pos()
    elif query == '10':
        city()
    elif query == '11':
        exit_q()
    else:
        inv_in()


def add_rev():
    os.system('cls')
    fn_email = input("Enter your email: ")
    mt_date = input("Enter match date: ")
    mt_home = input("Enter home team: ")
    mt_away = input("Enter away team: ")
    rating = input("Enter rating: ")
    text_rev = input("Enter your review: ")
    try:
        add_rev_sql = "INSERT INTO fan_review (fn_email, mt_date, mt_home, mt_away, rating, text_rev) VALUES(%s, %s, %s, %s, %s, %s)"
        dbhandler.execute(add_rev_sql, (fn_email, mt_date, mt_home, mt_away, rating, text_rev))
        connection.commit()
        exec_q()
    except db.IntegrityError:
        os.system('cls')
        print("Review Failed ... Choose: \n 1. Retry \n 2. Home Screen \n 3. Exit")
        rev_ch = input("Enter your Choice: ")
        if rev_ch == '1':
            add_rev()
        elif rev_ch == '2':
            home_function()
        else:
            exit_q()


def view_rev():
    os.system('cls')
    mt_date = input("Enter match date: ")
    mt_home = input("Enter home team: ")
    mt_away = input("Enter away team: ")
    dbhandler.execute(f"SELECT * FROM fan_review WHERE mt_date = '{mt_date}' AND mt_home = '{mt_home}' AND mt_away = '{mt_away}'")
    result = dbhandler.fetchall()
    for item in result:
        print(item)
    exec_q()


def register_function():
    os.system('cls')
    print("Registering New User: \n")
    email = input('Enter your email: ')
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    gender = input('Enter your gender as M or F: ')
    birthdate = input('Enter your birthdate in mm/dd/yyyy format: ')
    fav_club = input('Enter your favorite club: ')
    try:
        fan_sql = "INSERT INTO fan (fan_email, fan_username, fan_password, fan_gender, fan_birthdate, fan_fav_club_name) VALUES(%s, %s, %s, %s, %s, %s)"
        dbhandler.execute(fan_sql, (email, username, password, gender, birthdate, fav_club))
        connection.commit()
        user_queries()
    except db.IntegrityError:
        os.system('cls')
        print("Registration Failed ... Choose: \n 1. Retry \n 2. Home Screen \n 3. Exit")
        reg_ch = input("Enter your Choice: ")
        if reg_ch == '1':
            register_function()
        elif reg_ch == '2':
            home_function()
        else:
            exit_q()


def pl_nat():
    os.system('cls')
    nat = input("Enter nationality: ")
    dbhandler.execute(f"SELECT player_name, hist_club_name, pl_nationality FROM player_hist INNER JOIN player ON player.pl_name = player_hist.player_name AND player.pl_date_birth = player_hist.date_birth WHERE pl_nationality = '{nat}'")
    result = dbhandler.fetchall()
    for item in result:
        print(item)
    exec_q()


def top_team():
    os.system('cls')
    print("Choose Top 10 Teams By: "
          "\n 1. Matches Won"
          "\n 2. Home Matches Won"
          "\n 3. Yellow Cards"
          "\n 4. Fouls"
          "\n 5. Shots")
    top_ch = input("Enter your Choice: ")
    if top_ch == '1':
        dbhandler.execute(f"SELECT mt_won.clb_name_home, COUNT(*) FROM (SELECT clb_name_home FROM match_statistics WHERE goals_home > goals_away UNION ALL SELECT clb_name_away FROM match_statistics WHERE goals_home < goals_away) AS mt_won GROUP BY 1 ORDER BY 2 DESC LIMIT 10")
        result = dbhandler.fetchall()
        for item in result:
            print(item)
        exec_q()
    elif top_ch == '2':
        dbhandler.execute(f"SELECT COUNT(*), clb_name_home FROM match_statistics WHERE goals_home > goals_away GROUP BY clb_name_home ORDER BY 1 DESC LIMIT 10")
        result = dbhandler.fetchall()
        for item in result:
            print(item)
        exec_q()
    elif top_ch == '3':
        dbhandler.execute(f"SELECT mt_yellow.clb_name_home, SUM(mt_yellow.cards) FROM (SELECT clb_name_home, SUM(yellow_cards_home) AS cards FROM match_statistics GROUP BY 1 UNION ALL SELECT clb_name_away, SUM(yellow_cards_away) AS cards FROM match_statistics GROUP BY 1) AS mt_yellow GROUP BY 1 ORDER BY 2 DESC LIMIT 10")
        result = dbhandler.fetchall()
        for item in result:
            print(item)
        exec_q()
    elif top_ch == '4':
        dbhandler.execute(f"SELECT mt_foul.clb_name_home, SUM(mt_foul.fouls) FROM (SELECT clb_name_home, SUM(fouls_home) AS fouls FROM match_statistics GROUP BY 1 UNION ALL SELECT clb_name_away, SUM(fouls_away) AS fouls FROM match_statistics GROUP BY 1) AS mt_foul GROUP BY 1 ORDER BY 2 DESC LIMIT 10")
        result = dbhandler.fetchall()
        for item in result:
            print(item)
        exec_q()
    elif top_ch == '5':
        dbhandler.execute(f"SELECT mt_shot.clb_name_home, SUM(mt_shot.shots) FROM(SELECT clb_name_home, SUM(shots_home) AS shots FROM match_statistics GROUP BY 1 UNION ALL SELECT clb_name_away, SUM(shots_away) AS shots FROM match_statistics GROUP BY 1) AS mt_shot GROUP BY 1 ORDER BY 2 DESC LIMIT 10")
        result = dbhandler.fetchall()
        for item in result:
            print(item)
        exec_q()
    else:
        inv_in()


def top_team_season():
    os.system('cls')
    dbhandler.execute(f"SELECT mt_won.clb_name_home, mt_won.mtch_season, mt_won.season_wins FROM (SELECT clb_name_home, mtch_season, COUNT(*) AS season_wins FROM match_statistics WHERE goals_home > goals_away GROUP BY 1, 2 UNION ALL SELECT clb_name_away, mtch_season, COUNT(*) AS season_wins FROM match_statistics WHERE goals_home < goals_away GROUP BY 1,2 ORDER BY 3 DESC) AS mt_won GROUP BY 2")
    result = dbhandler.fetchall()
    for item in result:
        print(item)
    exec_q()


def team_view():
    os.system('cls')
    team_in = input("Enter the team's name: ")
    dbhandler.execute(f"SELECT * FROM club WHERE club.club_name = '{team_in}'")
    result = dbhandler.fetchall()
    for item in result:
        print(item)
    exec_q()


def pl_view():
    os.system('cls')
    pl_in = input("Enter player's name: ")
    dbhandler.execute(f"SELECT * FROM player WHERE pl_name = '{pl_in}'")
    result = dbhandler.fetchall()
    for item in result:
        print(item)
    exec_q()


def home_std():
    os.system('cls')
    std_in = input("Enter Stadium's Name: ")
    dbhandler.execute(f"SELECT club.club_name FROM club WHERE stadium_name = '{std_in}'")
    result = dbhandler.fetchall()
    for item in result:
        print(item)
    exec_q()


def pl_pos():
    os.system('cls')
    pos_in = input("Enter Players' Position: ")
    dbhandler.execute(f"SELECT * FROM player WHERE player.pl_position = '{pos_in}'")
    result = dbhandler.fetchall()
    for item in result:
        print(item)
    exec_q()


def city():
    os.system('cls')
    city_in = input("Enter City: ")
    dbhandler.execute(f"Select club.club_name FROM club INNER JOIN stadium ON club.stadium_name = stadium.std_name WHERE std_address LIKE '%{city_in}%'")
    result = dbhandler.fetchall()
    for item in result:
        print(item)
    exec_q()


def inv_in():
    os.system('cls')
    print("Invalid Option ... Choose: \n 1. Home Screen \n 2. Exit")
    invl = input("Enter your Choice: ")
    if invl == '1':
        home_function()
    else:
        exit_q()


def exec_q():
    print("\n Query Executed ... Choose: \n 1. Back to Options Menu \n 2. Home Screen \n 3. Exit")
    ex_ch = input("Enter your Choice: ")
    if ex_ch == '1':
        if user == 0 and guest == 1:
            guest_mode()
        else:
            user_queries()
    elif ex_ch == '2':
        home_function()
    elif ex_ch == '3':
        exit_q()
    else:
        inv_in()


def exit_q():
    os.system('cls')
    print("Exiting ...")
    time.sleep(1)
    connection.close()
    exit()


home_function()

# connection.close()
