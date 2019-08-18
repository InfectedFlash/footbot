from telebot import types
from bot_data import LEAGUES
from bot_functions import build_leagues_menu_btn


class InlineButtonGroup(types.InlineKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InlineButton(types.InlineKeyboardButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Buttons groups
# Main menu group

main_menu = InlineButtonGroup(row_width=3)
help_btn = InlineButton(text='Help', callback_data='help')
leagues_btn = InlineButton(text='Select league', callback_data='leagues')
matches_btn = InlineButton(text='See matches', callback_data='matches')

main_menu.row(help_btn)
main_menu.row(leagues_btn, matches_btn)

# Leagues menu group

leagues_menu_btn = build_leagues_menu_btn(InlineButtonGroup, InlineButton, LEAGUES, 2)
