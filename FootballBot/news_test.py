from bs4 import BeautifulSoup
import requests


class News:
    def __init__(self, title, text):

        self.text = text
        self.title = title

    def __str__(self):
        return ('{}\n' + '{}').format(self.title, self.text)

    def __repr__(self):
        return self.__str__()


def get_news_text(url):
    html = requests.get(url)
    data = html.text
    soup = BeautifulSoup(data, 'lxml')
    news_text = []
    temp = soup.find('div', class_='article-text').find_all('p')
    for i in temp:
        news_text.append(i.text.strip())
    return news_text


def get_news(url):
    if url == "LALIGA":
        url = 'http://football.ua/spain.html'

    elif url == "EPL":
        url = 'http://football.ua/england.html'

    elif url == "SERIA":
        url = 'http://football.ua/italy.html'

    elif url == 'LIGUE':
        url = 'http://football.ua/france.html'

    elif url == "BUNDESLIGA":
        url = 'http://football.ua/germany.html'
    html = requests.get(url)
    data = html.text
    soup = BeautifulSoup(data, 'lxml')
    temp = soup.find('div', id='ctl00_columnRight').find('ul').find_all('li', class_="")
    news = []
    for i in temp[0:3]:

        news_title = i.find('a').text
        news_text = get_news_text(i.find('a')['href'])
        new_new = News(news_title, ' '.join(news_text))
        news.append(new_new)
        print(new_new)
    return news


get_news('http://football.ua/france.html')
