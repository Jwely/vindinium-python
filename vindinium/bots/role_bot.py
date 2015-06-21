__author__ = 'Jwely'

import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import AStar


__all__ = ["RoleBot"]


class RoleBot(BaseBot):
    """ this bot makes decisions by weighing the value of the space
     it occupies, as well as the surrounding 4 spaces. It uses propensities
     to mine, drink, kill, and flee, which can be randomly altered to
     optimize the behavior.
     """

    def __init__(self, props = None):
        super(RoleBot, self).__init__()

        # propensities
        if props is None:
            props = {"mine" : 3.0,
                     "drink": 2.0,
                     "kill" : 1.0,
                     "flee" : 2.0}

        self.propensity_to = props

    def start(self):
        thought = "I am {0} with [id = {1}]".format(self.hero.name, self.hero.id)
        self._log_brainwave(thought, map = True)

        # defines multiple pathfinding strategies scaled to map size
        ms = float(self.game.map.size)
        self.search_aggressive = AStar(self.game.map, (-1), (ms / 4))       # prefers going through heroes
        self.search_default    = AStar(self.game.map, (ms / 16), (ms / 4))  # ignores heroes entirely
        self.search_cautious   = AStar(self.game.map, (ms / 8), (ms / 4))   # prefers going around heroes
        self.search_evade      = AStar(self.game.map, (ms / 4), (ms / 8))   # stays far away from heroes

        # sets the default search
        self._set_search()


    def _set_search(self, strategy = "d"):
        """ sets the default search strategy used when self.search is called """

        if strategy == "a":
            self.search = self.search_aggressive
        elif strategy == "d":
            self.search = self.search_default
        elif strategy == "c":
            self.search = self.search_cautious
        elif strategy == " e":
            self.search = self.search_evade
        else:
            self.search = self.search_default


    def move(self):

        # each of these are dictionaries who's values are arrays
        valid_moves = self._valid_moves()
        best_move = random.choice(valid_moves.keys())

        self._get_player_dists()



        self._log_brainwave("move: {0}".format(best_move), map = True)

        return best_move



    def _is_my_mine(self, x, y, mines):
        """ returns true if one of my mines are at coordinates """

        for mine in mines:
            if mine.x == x and mine.y == y:
                if mine.owner == self.hero.id:
                    return True
        return False


    def _is_occupied_by_player(self, x, y):
        heroes = self.game.heroes

        for hero in heroes:
            if hero.x == x and hero.y == y:
                return True
        return False


    @staticmethod
    def _pd(path_dist):
        """
        simple static method to make sure the bot never tries to divide by
        zero path distance. The value this returns with path_distance is below
        1 has large implications for how likely moves into players, taverns, mines
        will be.
        """
        if path_dist >= 1:
            return float(path_dist)
        else:
            return 0.5


    def _valid_moves(self) :
        """
        returns a dict of valid moves, with keys as directions and values as x,y coordinates
        """
        x = self.hero.x
        y = self.hero.y

        moves = {vin.STAY : (x, y),
                 vin.NORTH: (x, y - 1),
                 vin.WEST : (x - 1, y),
                 vin.EAST : (x + 1, y),
                 vin.SOUTH: (x, y + 1)}

        valid_moves = {}
        for key in moves:
            try:
                if self.game.map[moves[key]] != vin.TILE_WALL:
                    valid_moves[key] = moves[key]
            except IndexError:
                pass

        return valid_moves


    def _get_player_dists(self):
        """ determines distances between every hero and every other hero"""

        for hero in self.game.heroes:
            x = hero.x
            y = hero.y
            hero.dist_to_heroes = vin.utils.order_by_distance2(x, y , self.game.heroes, self.game.map)
        return


    def _go_to_nearest_tavern(self):
        x = self.hero.x
        y = self.hero.y

        # Order taverns by distance
        taverns = vin.utils.order_by_distance(x, y, self.game.taverns, self.game.map)
        for tavern in taverns:
            command = self._go_to(tavern.x, tavern.y)

            if command:
                return command

        return self._random()


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