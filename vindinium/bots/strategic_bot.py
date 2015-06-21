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

    def __init__(self, props = None):
        super(StrategicBot, self).__init__()

        # propensities
        if props is None:
            props = {"mine" : 3.0,
                     "drink": 2.0,
                     "kill" : 1.0,
                     "flee" : 2.0}

        self.propensity_to = props
        self.move_history  = ["Start"]


    def start(self):
        print("I am {0} with id: {1}".format(self.hero.name, self.hero.id))
        self.search = AStar(self.game.map)


    def move(self):

        # each of these are dictionaries who's values are arrays
        valid_moves = self._valid_moves()
        move_values = {}

        # this dict will house the final scores, where values are floats
        move_scores  = {}

        # find the values of all valid moves
        for key in valid_moves:
            x1 = valid_moves[key][0]
            y1 = valid_moves[key][1]
            move_values[key] = self._total_value_of_point(x1, y1)
            move_scores[key] = sum(move_values[key])

        # final decision time!
        v = list(move_scores.values())
        k = list(move_scores.keys())

        best_move = k[v.index(max(v))]

        # prevent getting stuck
        if len(self.move_history) >= 5:
            hist_len = 5
        else:
            hist_len = len(self.move_history)

        if all([best_move == pm for pm in self.move_history[-hist_len:]]):
            best_move = random.choice(move_values.keys())

        # print the decision
        message = "moved {0}  F:{1:.2f}  K:{2:.2f}  D:{3:.2f}  M:{4:.2f}  HP:{5}".format(
                    best_move, move_values[best_move][0], move_values[best_move][1],
                    move_values[best_move][2], move_values[best_move][3], self.hero.life)

        print(message)
        self.move_history.append(message)

        return best_move


    def _valid_moves(self) :
        x = self.hero.x
        y = self.hero.y

        moves = {vin.STAY : (x, y),
                 vin.NORTH: (x, y - 1),
                 vin.WEST : (x - 1, y),
                 vin.EAST : (x + 1, y),
                 vin.SOUTH: (x, y + 1)}

        valid_moves = {}
        for key in moves:
            if self.game.map[moves[key]] != vin.TILE_WALL:
                valid_moves[key] = moves[key]

        return valid_moves


    def _total_value_of_point(self, x, y):


        values = [self.propensity_to["flee"] * self._flee_value_of_point(x, y),
                  self.propensity_to["kill"] * self._kill_value_of_point(x, y),
                  self.propensity_to["drink"] * self._drink_value_of_point(x, y),
                  self.propensity_to["mine"] * self._mine_value_of_point(x, y)]

        # set anything less than 0.1 to 0.1
        values = [v if v > 0.1 else 0.1 for v in values]

        return values


    def _flee_value_of_point(self, x, y):
        """
        When the hero has low health, tiles with good flee value are
        those that are further away from enemy players. This becomes
        especially true if the hero has lots of mines at the moment
        """

        players = [p for p in self.game.heroes if p.id != self.hero.id]
        players = vin.utils.order_by_distance(x, y, players, self.game.map)

        appeals = [1 + (float(p.path_dist) ** 0.25) * (100 - self.hero.life) / 100 for p in players]
        appeal = sum(appeals) * (self.hero.mine_count / len(self.game.mines))

        # bad tiles
        t_spawn = self.game.map[x, y] == vin.TILE_SPAWN
        t_tavern = self.game.map[x, y] == vin.TILE_TAVERN
        t_mine   = self.game.map[x, y] == vin.TILE_MINE
        t_player = self._is_occupied_by_player(x, y)

        if t_spawn or t_tavern or t_mine or t_player:
            return 0
        else:
            return appeal


    def _kill_value_of_point(self, x, y):
        """
        good kill value points are close to players with low
        health but lots of mines. But also away from taverns.
        wealthy players with high health can cause negative kill value
        """

        players = [p for p in self.game.heroes if p.id != self.hero.id]
        players = vin.utils.order_by_distance(x, y, players, self.game.map)

        appeals = [p.mine_count * (100 - p.life) / (self._pd(p.path_dist)) for p in players]
        appeal = sum(appeals)

        # if bot is right next to another player, who is closer to the tavern?
        if players[0].path_dist >= 2:
                me_taverns = vin.utils.order_by_distance(self.hero.x, self.hero.y,
                                                         self.game.taverns, self.game.map)
                me_min_dist = me_taverns.dist_path
                he_taverns = vin.utils.order_by_distance(players[0].x, players[0].y,
                                                         self.game.taverns, self.game.map)
                he_min_dist = he_taverns.dist_path

                enemy_closer_to_tavern  =  me_min_dist <= he_min_dist
        else:
            enemy_closer_to_tavern = False


        # bad tiles
        t_spawn = self.game.map[x, y] == vin.TILE_SPAWN
        t_tavern = self.game.map[x, y] == vin.TILE_TAVERN
        t_mine   = self.game.map[x, y] == vin.TILE_MINE

        # condition

        if t_spawn or t_tavern or t_mine or enemy_closer_to_tavern:
            return 0
        else:
            return appeal

    def _drink_value_of_point(self, x, y):
        """
        determined by distance to closest tavern and health of hero.
        Getting closer to a tavern becomes more important when health is
        bellow 50.
        """

        # orders taverns by path distance from input xy
        taverns = vin.utils.order_by_distance(x, y, self.game.taverns, self.game.map)
        path_dist = taverns[0].path_dist

        # calculate the final appeal
        if self.hero.life > 60:
            fac = 1
        elif self.hero.life >40:
            fac = 3
        else:
            fac = 9

        appeal = fac * (100 - self.hero.life) / (10 * self._pd(path_dist))

        # bad tiles
        t_spawn = self.game.map[x, y] == vin.TILE_SPAWN
        t_tavern = self.game.map[x, y] == vin.TILE_TAVERN
        t_mine   = self.game.map[x, y] == vin.TILE_MINE
        t_player = self._is_occupied_by_player(x, y)

        if t_spawn or t_mine or t_player:
            return 0
        elif t_tavern:
            return appeal * 2
        else:
            return appeal


    def _mine_value_of_point(self, x, y):
        """ determined by distance to 4 closest mines """

        # orders mines by shortest path distance and removes those owned by this bot
        mines = vin.utils.order_by_distance(x, y, self.game.mines, self.game.map)
        bad_mines = []
        for mine in mines:
            if mine.owner != self.hero.id:
                bad_mines.append(mine)

        path_dists = [m.path_dist for m in bad_mines]

        # calculate the final appeal for mines and mine clusters
        if len(path_dists) == 0:
            return 0

        elif len(path_dists) >= 4:
            appeal = (8 / self._pd(path_dists[0]) +
                      4 / self._pd(path_dists[1]) +
                      2 / self._pd(path_dists[2]) +
                      1 / self._pd(path_dists[3]))

        else:
            appeal = 8 / self._pd(path_dists[0])

        # bad tiles
        t_spawn = self.game.map[x, y] == vin.TILE_SPAWN
        t_tavern = self.game.map[x, y] == vin.TILE_TAVERN
        t_mine   = self.game.map[x, y] == vin.TILE_MINE
        t_player = self._is_occupied_by_player(x, y)

        if t_spawn or t_tavern or t_player:
            return 0
        elif t_mine:
            if self._is_my_mine(x, y, mines):
                return 0
            else:
                return appeal * 2
        else:
            return appeal


    def _is_my_mine(self, x, y, mines):
        """ returns true if one of my mines are at coordinates """

        for mine in mines:
            if mine.x == x and mine.y == y:
                if mine.owner == self.hero.id:
                    print("I already own this mine")
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