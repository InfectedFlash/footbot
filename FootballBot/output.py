#!/usr/bin/python3.6
import re
import mysql.connector


def show_info(country):
    conn = mysql.connector.connect(host='localhost',
                                   database='football',
                                   user='root',
                                   password='motros1988')

    cursor = conn.cursor()

    query = ("""SELECT * FROM `team`
                   WHERE team_country = '%s'
                ORDER BY team_position
                """) % (country)

    cursor.execute(query)

    message = ""
    for team in cursor:
        message += str(team[1]) + "|" + team[2] + "     " + str(team[3]) + "\n"

    print(message)




show_info("Англия")