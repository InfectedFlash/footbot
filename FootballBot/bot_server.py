"""This module is server for bot"""

import cherrypy
import requests
import telebot

from bot_config import token


foot_bot = telebot.TeleBot(token)

WEBHOOK_HOST = '109.120.159.28'
WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '109.120.159.28'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '../../webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = '../../webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % token


FOOT_BOT_ADDRESS = "http://127.0.0.1:7771"

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


class WebhookServer(object):

    # Первый бот (название функции = последняя часть URL вебхука)
    @cherrypy.expose
    def footbot(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            # Вот эта строчка и пересылает все входящие сообщения на нужного бота
            requests.post(FOOT_BOT_ADDRESS, data=json_string)
            return ''
        else:
            raise cherrypy.HTTPError(403)


# bot.remove_webhook()
#
#
# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                 certificate=open(WEBHOOK_SSL_CERT, 'r'))


# cherrypy.config.update({
#     'server.socket_host': WEBHOOK_LISTEN,
#     'server.socket_port': WEBHOOK_PORT,
#     'server.ssl_module': 'builtin',
#     'server.ssl_certificate': WEBHOOK_SSL_CERT,
#     'server.ssl_private_key': WEBHOOK_SSL_PRIV
# })


cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})


if __name__ == '__main__':

    foot_bot.remove_webhook()
    foot_bot.set_webhook(url='https://122.122.122.122/AAAA',
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

    # bot_2.remove_webhook()
    # bot_2.set_webhook(url='https://122.122.122.122/ZZZZ',
    #                 certificate=open(WEBHOOK_SSL_CERT, 'r'))

    cherrypy.config.update({
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': WEBHOOK_SSL_CERT,
        'server.ssl_private_key': WEBHOOK_SSL_PRIV,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
