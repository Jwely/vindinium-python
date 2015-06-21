__author__ = 'Jwely'

import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import AStar


__all__ = ["StrategicBot"]


class StrategicBot(BaseBot):
    """ this bot makes decisions by weighing the value of the space
     it occupies, as well as the surrounding 4 spaces. It uses propensities
     to mine, drink, kill, and flee, which can be randomly altered to
     optimize the behavior.
     """

    def __init__(self):
        super(StrategicBot, self).__init__()

        # propensities
        p = {"mine" : 1,
             "drink": 1,
             "kill" : 1,
             "flee" : 1}

        self.hero.propensities = p


    def start(self):
        self.search = AStar(self.game.map)


    def move(self):
        return self._random()


    def _mining_value(self, direction):
        x = self.hero.x
        y = self.hero.y

        # orders mines by distance and removes those owned by this bot
        mines = vin.utils.order_by_distance(x, y, self.game.mine)
        for mine in mines:
            if mine.owner == self.hero.id:
                mines.remove(mine)


    def _go_to(self, x_, y_):
        x = self.hero.x
        y = self.hero.y

        # Compute path to the mine
        path = self.search.find(x, y, x_, y_)

        # Send command to follow that path
        if path is None:
            return

        elif len(path) > 0:
            x_, y_ = path[0]

        return vin.utils.path_to_command(x, y, x_, y_)

    def _random(self):
        return random.choice(['Stay', 'North', 'West', 'East', 'South'])