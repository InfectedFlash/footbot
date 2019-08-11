#!/usr/bin/python3.6

import datetime
import cherrypy
import re
import requests
import telebot

from bs4 import BeautifulSoup
from datetime import timedelta
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
from telebot import types


# 195940
token = '516132326:AAHvfpUAsy-IMEdnMFJ9Gi21Do3OxHGyJIg'
bot = telebot.TeleBot(token)


# WEBHOOK_HOST = '206.189.204.244'
# WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
# WEBHOOK_LISTEN = '206.189.204.244'  # На некоторых серверах придется указывать такой же IP, что и выше
#
# WEBHOOK_SSL_CERT = '../webhook_cert.pem'  # Путь к сертификату
# WEBHOOK_SSL_PRIV = '../webhook_pkey.pem'  # Путь к приватному ключу
#
# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/%s/" % token
#
#
# class WebhookServer(object):
#     @cherrypy.expose
#     def index(self):
#         if 'content-length' in cherrypy.request.headers and \
#                         'content-type' in cherrypy.request.headers and \
#                         cherrypy.request.headers['content-type'] == 'application/json':
#             length = int(cherrypy.request.headers['content-length'])
#             json_string = cherrypy.request.body.read(length).decode("utf-8")
#             update = telebot.types.Update.de_json(json_string)
#             # Эта функция обеспечивает проверку входящего сообщения
#             bot.process_new_updates([update])
#             return ''
#         else:
#             raise cherrypy.HTTPError(403)


@bot.message_handler(func=lambda message: True, commands=['top1', 'top2', 'top3', 'top4', 'top5', 'top6', 'top7',
                                                          'top8', 'top9', 'top10', 'top11', 'top12', 'top13', 'top14',
                                                          'top15', 'top16', 'top17', 'top18', 'top19', 'top20'])
def bot_message(message):
    i = re.search(r"\d+", message.text)
    i = int(i.group(0))
    bot.reply_to(message, "Preparing Results")
    bot.reply_to(message, get_matches(i, l="0"))


@bot.message_handler(func=lambda message: True, commands=['res1', 'res2', 'res3', 'res4', 'res5', 'res6', 'res7',
                                                          'res8', 'res9', 'res10', 'res11', 'res12', 'res13', 'res14',
                                                          'res15', 'res16', 'res17', 'res18', 'res19', 'res20'])
def bot_message(message):
    i = re.search(r"\d+", message.text)
    i = int(i.group(0))
    bot.reply_to(message, "Preparing Results")
    bot.reply_to(message, get_matches(i, l="0", temp_date="yesterday"))


@bot.message_handler(func=lambda message: True, commands=['next1', 'next2', 'next3', 'next4', 'next5', 'next6', 'next7',
                                                          'next8', 'next9', 'next10', 'next11','next12', 'next13',
                                                          'next14', 'next15', 'next16', 'next17', 'next18', 'next19',
                                                          'next20'])
def bot_message(message):
    i = re.search(r"\d+", message.text)
    i = int(i.group(0))
    bot.reply_to(message, "Preparing Results")
    bot.reply_to(message, get_matches(i, l="0", temp_date="tomorrow"))


@bot.message_handler(func=lambda message: True, commands=['live{}'.format(i) for i in range(1, 21)])
def bot_message(message):
    i = re.search(r"\d+", message.text)
    i = int(i.group(0))
    bot.reply_to(message, "Preparing Results")
    bot.reply_to(message, get_matches(i, l="1"))


@bot.message_handler(func=lambda message: True, commands=["standings"])
def on_ping(message):

    bot.reply_to(message, "Type /apl /laliga /bundesliga /ligue1 /seriaA")


@bot.message_handler(func=lambda message: True, commands=["apl", "laliga", "bundesliga", "ligue1", "seriaA"])
def on_ping(message):
    url = re.search(r'\w+', message.text)
    url = url.group(0).upper()
    if url == "LALIGA":
        url = 'https://all.soccer/ru/tournament/1667580/standings'

    elif url == "APL":
        url = 'https://all.soccer/ru/tournament/1647270/standings'

    elif url == "SERIAA":
        url = 'https://all.soccer/ru/tournament/1688055/standings'

    elif url == 'LIGUE1':
        url = 'https://all.soccer/ru/tournament/1647277/standings'

    elif url == "BUNDESLIGA":
        url = 'https://all.soccer/ru/tournament/1661159/standings'
    bot.reply_to(message, get_standings(url))


@bot.message_handler(func=lambda message: True, commands=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="APL", callback_data=get_standings(url))
    keyboard.add(callback_button)
    keyboard.add(callback_button)
    bot.send_message(message, "Test", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, """Hey, you!!
Type /top1-20 to see top(1-20) teams
Type /live1-20 to see LIVE - top(1-20) teams
Type /res1-20 to see top(1-20) teams yesterday results
Type /next1-20 to see top(1-20) teams tomorrow matchs
Type /standings to see current stands""")



# @bot.message_handler(content_types=["text"])
# def welcom(message):
#     bot.send_message(message.chat.id, "Hey, you!!" + "\n" + "Type /top1-20 to see top(1-20) teams" + "\n" + "Type /live1-20 to see LIVE - top(1-20) teams" + "\n" + "Type /res1-20 to see top(1-20) teams yesterday results" + "\n" + "Type /next1-20 to see top(1-20) teams tomorrow matchs" + "\n" + "Type /standings to see current stands")


i = ""

thatday = datetime.datetime.today()
yesterday = thatday - timedelta(1)
tomorrow = thatday + timedelta(1)
tomorrow = tomorrow.strftime("%d.%m.%Y")
thatday = thatday.strftime("%d.%m.%Y")
yesterday = yesterday.strftime("%d.%m.%Y")


def get_matches(num_top=5, l="0", temp_date="today"):
    today_match = []
    all_teams = []
    c_date = datetime.datetime.today()
    if temp_date == "tomorrow":
        c_date = c_date + timedelta(1)
    elif temp_date == "yesterday":
        c_date = c_date - timedelta(1)

    c_date = c_date.strftime("%d.%m.%Y")

    def get_tops(url):
        html = requests.get(url)
        data = html.text
        soup = BeautifulSoup(data, 'lxml')
        teams = []
        top_teams = soup.find_all('td', class_='col-2', text='')
        top_teams = top_teams[0:num_top]
        for team in top_teams:
            teams.append(team.text.strip())
        return teams

    urls = ('https://all.soccer/ru/tournament/12353/standings', 'https://all.soccer/ru/tournament/12317/standings', 'https://all.soccer/ru/tournament/12323/standings', 'https://all.soccer/ru/tournament/872508/standings', 'https://all.soccer/ru/tournament/12225/standings')
    for url in urls:
        teams = get_tops(url)
        all_teams = all_teams + teams

    html = requests.get('https://all.soccer/ru?live=' + l + '&date=' + c_date + '&show_my_turnir=0&my_games=0&sort=1&odds=0')
    data = html.text
    soup = BeautifulSoup(data, 'lxml')

    b_message = ""
    ma = soup.find_all('tr', class_='match-row')
    for match in ma:
        try:
            status = match.find('td', class_='match-status').find('span', class_='status').text
        except Exception:
            status = ""
        current_match = dict(
            time=match.find('td', class_='match-time').text.strip(),
            status=status,
            home_team=match.find('td', class_='home-team').text.strip(),
            score=match.find('td', class_='score').text.strip(),
            visit_team=match.find('td', class_='visit-team').text.strip(),
            competition=match.findPreviousSiblings('tr', class_='turnir-name')[0].text.strip()
            )

        if current_match['home_team'] in all_teams or current_match['visit_team'] in all_teams:
            today_match.append(current_match)
    #print(current_match.get('competition'))

    newlist = sorted(today_match, key=lambda k: k['time'])
    for current_match in newlist:

        b_message += (current_match.get('time') + "| " + current_match.get('home_team') + " " +
                      current_match.get('score') + " " + current_match.get('visit_team') + " (" +
                      current_match.get('competition') + ") " + current_match.get('status')+"\n")

    return b_message


def get_standings(url):

    #num_top = int(input("How match positions?  "))
    html = requests.get(url)
    data = html.text
    soup = BeautifulSoup(data, 'lxml')
    stand = soup.find('table', class_='site-default-table').find_all('tr', class_='table-row')
    stand_head = soup.find('table', class_='site-default-table').find('tr')
    stands = []
    for pos in stand:
        current_pos = dict(
            position=int(pos.find('td', class_='col-1').text.strip()),
            team=pos.find('td', class_='col-2').text.strip(),
            games=pos.find('td', class_='col-3').text.strip(),
            wins=pos.find('td', class_='col-4').text.strip(),
            draws=pos.find('td', class_='col-5').text.strip(),
            looses=pos.find('td', class_='col-6').text.strip(),
            goals=pos.find('td', class_='col-7').text.strip(),
            points=pos.find('td', class_='col-8').text.strip(),
        )
        stands.append(current_pos)
    stand_head = dict(
        position=stand_head.find('th', class_='col-1').text.strip(),
        team=stand_head.find('th', class_='col-2').text.strip(),
        games=stand_head.find('th', class_='col-3').text.strip(),
        wins=stand_head.find('th', class_='col-4').text.strip(),
        draws=stand_head.find('th', class_='col-5').text.strip(),
        looses=stand_head.find('th', class_='col-6').text.strip(),
        goals=stand_head.find('th', class_='col-7').text.strip(),
        points=stand_head.find('th', class_='col-8').text.strip(),
    )

    newlist = sorted(stands, key=lambda k: k['position'])
    #newlist = newlist[:num_top]

    b_message_width = []
    for current_pos in newlist:
        b_message_width.append(len(current_pos.get('team')))
    width = max(b_message_width) + 10
    incr2 = 2

    b_message = PrettyTable()
    b_message.field_names = ["Team", "Games", "Points"]
    b_message.align = 'l'
    b_message.set_style(MSWORD_FRIENDLY)
    b_message.border = False
    b_message
    for current_pos in newlist:
        b_message.add_row([current_pos.get('team'), current_pos.get('games'), current_pos.get('points')])

    return b_message,\
           b_message


# bot.remove_webhook()
#
#
# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                 certificate=open(WEBHOOK_SSL_CERT, 'r'))
#
#
# cherrypy.config.update({
#     'server.socket_host': WEBHOOK_LISTEN,
#     'server.socket_port': WEBHOOK_PORT,
#     'server.ssl_module': 'builtin',
#     'server.ssl_certificate': WEBHOOK_SSL_CERT,
#     'server.ssl_private_key': WEBHOOK_SSL_PRIV
# })
#
#
# cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})


if __name__ == '__main__':
    bot.polling(none_stop=True)



# for current_pos in newlist:
    #     incr = width - len(current_pos.get('team')) - 2
    #     b_message += '{} {} {:{fill}{align}{incr}} {:{align}{incr2}}'.format(str(current_pos.get('position')), current_pos.get('team'),  current_pos.get('games'), current_pos.get('points'),fill='_', incr=incr, incr2=incr2, align='>') + "\n"
    #
    # h_message = (stand_head.get('position') + " " + stand_head.get('team') + "                       " + stand_head.get('games') + "/ " + stand_head.get('points') + "/ " + '\n' + b_message)
