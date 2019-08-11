#!/usr/bin/python3.6
import datetime
import re
from datetime import timedelta

import mysql.connector
import requests
from bs4 import BeautifulSoup


def get_info():
    conn = mysql.connector.connect(host='localhost',
                                   database='admin_footbot',
                                   user='admin_ad',
                                   password='motros1988')

    cursor = conn.cursor()

    print(cursor)
    urls = ['https://all.soccer/ru/tournament/12225/standings',
            'https://all.soccer/ru/tournament/872508/standings',
            'https://all.soccer/ru/tournament/12353/standings',
            'https://all.soccer/ru/tournament/12317/standings',
            'https://all.soccer/ru/tournament/12323/standings',
            'https://all.soccer/ru/tournament/12217/standings',
            'https://all.soccer/ru/tournament/12409/standings']

    matches = []
    teams = []

    for url in urls:
        html = requests.get(url)
        data = html.text
        soup = BeautifulSoup(data, 'lxml')
        stand = soup.find('table', class_='site-default-table').find_all('tr', class_='table-row')
        # print(stand)
        for pos in stand:
            current_team = dict(
                team_id=int(re.search(r"\d+", (pos.find('td', class_='col-2').find('a').get('href')))[0]),
                position=int(pos.find('td', class_='col-1').text.strip()),
                name=pos.find('td', class_='col-2').text.strip(),
                games=pos.find('td', class_='col-3').text.strip(),
                wins=pos.find('td', class_='col-4').text.strip(),
                draws=pos.find('td', class_='col-5').text.strip(),
                looses=pos.find('td', class_='col-6').text.strip(),
                goals=pos.find('td', class_='col-7').text.strip(),
                points=int(pos.find('td', class_='col-8').text.strip()),
                country=soup.find("span", class_='t-country').text.strip(),
                competition=soup.find('div', class_='site-title').text.strip()
            )
            print(current_team)
            teams.append(current_team)

    for team in teams:
        add_team = ("""INSERT team
                    (team_position, team_name, team_points, team_country, team_id)
                    VALUES ('%s', '%s', '%s', '%s', '%d')
                    ON DUPLICATE KEY UPDATE team_position = '%d', team_points = '%d'"""
                    % (team['position'], team['name'], team['points'], team['country'], int(team['team_id']),
                       team['position'], team['points']))

        upd_team = ("""UPDATE team
                      SET team_position = %d,
                          team_points = %d   
                     WHERE team_id = %d """
                    % (int(team['position']), int(team['points']), team['team_id']))

        cursor.execute(add_team)

    c_date = datetime.datetime.today()
    tommorow = c_date + timedelta(1)
    yesterday = c_date - timedelta(1)
    c_date = c_date.strftime("%d.%m.%Y")
    tommorow = tommorow.strftime("%d.%m.%Y")
    yesterday = yesterday.strftime("%d.%m.%Y")
    match_dates = [c_date, tommorow, yesterday]
    all_matches = []

    for date in match_dates:
        html = requests.get('https://all.soccer/ru?live=0&date=' + date + '&show_my_turnir=0&my_games=0&sort=1&odds=0')
        data = html.text
        soup = BeautifulSoup(data, 'lxml')
        ma = soup.find_all('tr', class_='match-row')
        for match in ma:
            status = " "
            try:
                status = match.find('td', class_='match-status').find('span', class_='status').text
            except Exception:
                pass

            try:
                status = \
                re.findall(r'\d', match.find('td', class_='match-status').find('span', class_='live-status').text)[0]
            except Exception:
                pass

            query = """SELECT team_id FROM `team` WHERE team_country = %s OR team_country = %s OR team_country = %s 
            OR team_country = %s OR team_country = %s"""
            query_data = ("Англия", "Испания", "Франция", "Италия", "Германия")
            cursor.execute(query, query_data)
            print(cursor)
            countries = cursor.fetchall()
            print(countries)
            current_match = dict(
                time=match.find('td', class_='match-time').text.strip(),
                status=status,
                home_team=int(re.search(r"\d+", (match.find('td', class_='home-team').find('a').get('href')))[0]),
                home_team_name=match.find('td', class_='home-team').text.strip(),
                score=match.find('td', class_='score').text.strip(),
                visit_team=int(re.search(r"\d+", (match.find('td', class_='visit-team').find('a').get('href')))[0]),
                visit_team_name=match.find('td', class_='visit-team').text.strip(),
                id=int(match.get('match_id')),
                competition=match.findPreviousSiblings('tr', class_='turnir-name')[0].text.strip(),
                date=date
            )
            all_matches.append(current_match)
            cursor.execute("""SELECT team_id FROM `team` WHERE team_id = '%s'""" % (current_match['home_team']))
            count = cursor.fetchone()
            print(count, type(count))
            if count is None:
                add_team = """INSERT INTO team (team_id, team_name) VALUES (%s, %s)"""
                add_team_data = (current_match['home_team'], current_match['home_team_name'])
                cursor.execute(add_team, add_team_data)
            cursor.execute("""SELECT team_id FROM `team` WHERE team_id = '%s'""" % (current_match['visit_team']))
            count = cursor.fetchone()
            if count is None:
                add_team = """INSERT INTO team (team_id, team_name) VALUES (%s, %s)"""
                add_team_data = (current_match['visit_team'], current_match['visit_team_name'])
                cursor.execute(add_team, add_team_data)

    for match in all_matches:
        add_match = (""" INSERT INTO `match`    
                (match_id, match_home_team, match_visit_team, match_status,
                match_time, match_score, match_competition, match_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE match_status = %s, match_date = %s, match_score = %s""")
        data = (match['id'], match['home_team'], match['visit_team'], match['status'],
                match['time'], match['score'], match['competition'], match['date'], match['status'],
                match['date'], match['score'])

        cursor.execute(add_match, data)

    conn.commit()
    cursor.close()
    conn.close()


get_info()
