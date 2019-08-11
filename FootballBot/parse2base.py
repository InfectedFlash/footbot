class Country():
    def __init__(self, name):
        self.name = name

    def __getattribute__(self, item):
        self.name = item


class Turnament():
    def __init__(self, name, country):
        self.name = name
        self.country = country

    def __str__(self):
        return "{}: {}".format(self.country, self.name)

    def __repr__(self):
        return self.__str__()

class Team():
    def __init__(self, name, points, position, wins, looses, draws, id):
        self.name = name
        self.points = points
        self.position = position
        self.wins = wins
        self.looses = looses
        self.draws = draws
        self.id = id


    def __str__(self):
        return "{}, {}".format(self.name, self.position)


spain = Turnament("Laliga", 'Spain')
new_team = Team('tot', 54, 2 , 2, 5, 5, 13434)


print(new_team)