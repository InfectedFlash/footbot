LEAGUES = {
    'laliga': {
        'country': 'Spain',
        'name': 'La Liga',
        'standings': 'https://all.soccer/ru/tournament/1667580/standings',
    },
    'apl': {
        'country': 'England',
        'name': 'Premier League',
        'standings': 'https://all.soccer/ru/tournament/1647270/standings',
    },
    'bundesliga': {
        'country': 'Germany',
        'name': 'Bundesliga',
        'standings': 'https://all.soccer/ru/tournament/1661159/standings',
    },
    'seriaA': {
        'country': 'Italy',
        'name': 'Seria A',
        'standings': 'https://all.soccer/ru/tournament/1688055/standings',
    },
    'ligue1': {
        'country': 'France',
        'name': 'Ligue 1',
        'standings': 'https://all.soccer/ru/tournament/1647277/standings',
    }
}

# Bot commands
COMMANDS = {
    'TOP': [f'top{i}' for i in range(1, 21)],
    'RESULTS': [f'res{i}' for i in range(1, 21)],
    'NEXT': [f'next{i}' for i in range(1, 21)],
    'LIVE': [f'live{i}' for i in range(1, 21)],
    'STANDINGS': ["standings"],
}

