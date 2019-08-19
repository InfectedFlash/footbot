
import cherrypy
import telebot
from datetime import datetime, timedelta

from bot_config import token
# from bot_output import bot
from bot_data import COMMANDS, LEAGUES
from bot_ui import buttons
bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda message: True, commands=['text'])
def bot_message(message):
    i = re.search(r"\d+", message.text)
    i = int(i.group(0))
    bot.reply_to(message, "Preparing Results")
    bot.reply_to(message, get_matches(i, l="0"))


@bot.message_handler(func=lambda message: True, commands=COMMANDS['RESULTS'])
def bot_message(message):
    i = re.search(r"\d+", message.text)
    i = int(i.group(0))
    bot.reply_to(message, "Preparing Results")
    bot.reply_to(message, get_matches(i, l="0", temp_date="yesterday"))


@bot.message_handler(func=lambda message: True, commands=COMMANDS['NEXT'])
def bot_message(message):
    i = re.search(r"\d+", message.text)
    i = int(i.group(0))
    bot.reply_to(message, "Preparing Results")
    bot.reply_to(message, get_matches(i, l="0", temp_date="tomorrow"))


@bot.message_handler(func=lambda message: True, commands=COMMANDS['LIVE'])
def bot_message(message):
    i = re.search(r"\d+", message.text)
    i = int(i.group(0))
    bot.reply_to(message, f"Preparing Results for {i}")
    # bot.reply_to(message, get_matches(i, l="1"))


@bot.message_handler(func=lambda message: True, commands=COMMANDS['STANDINGS'])
def on_ping(message):
    bot.reply_to(message, "Type /apl /laliga /bundesliga /ligue1 /seriaA")


@bot.message_handler(func=lambda message: True, commands=LEAGUES.keys())
def on_ping(message):
    url_pattern = re.search(r'\w+', message.text)
    url_key = url_pattern.group(0)
    url = LEAGUES[url_key]['url']
    bot.reply_to(message, get_standings(url))


@bot.message_handler(func=lambda message: True, commands=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="APL", callback_data=get_standings(url))
    keyboard.add(callback_button)
    keyboard.add(callback_button)
    bot.send_message(message, "Test", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def test_call(call):
    print(call.data)


@bot.callback_query_handler(func=lambda call: call.data == 'matches')
def test_call(call):
    print(call.data)
    c = 5
    while c > 0:
        c -= 1
        time.sleep(5.0)
        bot.send_message(call.message.chat.id, text=f'call_data is {call.data}')
    bot.send_message(call.message.chat.id, text='While ended')


@bot.callback_query_handler(func=lambda call: call.data == 'leagues')
def test_call(call):
    print(call.data)
    bot.send_message(call.message.chat.id, text='Choose league', reply_markup=buttons.build_leagues_menu_btn)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    #     bot.reply_to(message, """Hey, you!!
    # Type /top1-20 to see top(1-20) teams
    # Type /live1-20 to see LIVE - top(1-20) teams
    # Type /res1-20 to see top(1-20) teams yesterday results
    # Type /next1-20 to see top(1-20) teams tomorrow matchs
    # Type /standings to see current stands""")
    bot.send_message(message.chat.id, reply_markup=buttons.main_menu, text='Hello!')


# @bot.message_handler(content_types=["text"])
# def welcom(message):
#     bot.send_message(message.chat.id, "Hey, you!!" + "\n" + "Type /top1-20 to see top(1-20) teams" + "\n" + "Type /live1-20 to see LIVE - top(1-20) teams" + "\n" + "Type /res1-20 to see top(1-20) teams yesterday results" + "\n" + "Type /next1-20 to see top(1-20) teams tomorrow matchs" + "\n" + "Type /standings to see current stands")


i = ""

thatday = datetime.today()
yesterday = thatday - timedelta(1)
tomorrow = thatday + timedelta(1)
tomorrow = tomorrow.strftime("%d.%m.%Y")
thatday = thatday.strftime("%d.%m.%Y")
yesterday = yesterday.strftime("%d.%m.%Y")


def get_matches(num_top=5, l="0", temp_date="today"):
    today_match = []
    all_teams = []
    c_date = datetime.today()
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

    urls = (i.url for i in LEAGUES.items())
    for url in urls:
        teams = get_tops(url)
        all_teams = all_teams + teams

    html = requests.get(
        'https://all.soccer/ru?live=' + l + '&date=' + c_date + '&show_my_turnir=0&my_games=0&sort=1&odds=0')
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
    # print(current_match.get('competition'))

    newlist = sorted(today_match, key=lambda k: k['time'])
    for current_match in newlist:
        b_message += (current_match.get('time') + "| " + current_match.get('home_team') + " " +
                      current_match.get('score') + " " + current_match.get('visit_team') + " (" +
                      current_match.get('competition') + ") " + current_match.get('status') + "\n")

    return b_message


def get_standings(url):
    # num_top = int(input("How match positions?  "))
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
    # newlist = newlist[:num_top]

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

    return b_message, \
           b_message


class WebhookServer(object):
    # index равнозначно /, т.к. отсутствию части после ip-адреса (грубо говоря)
    @cherrypy.expose
    def index(self):
        
        length = int(cherrypy.request.headers['content-length'])
        json_string = cherrypy.request.body.read(length).decode("utf-8")
        print(json_string)
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 7771,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
