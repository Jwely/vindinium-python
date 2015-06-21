import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import AStar

__all__ = ['HunterBot']


class HunterBot(BaseBot):
    """ this bot hunts the juiciest player"""
    
    search = None

    def start(self):
        self.search = AStar(self.game.map)


    def move(self):

        # prioritize targets
        targets = self._prioritize_bounties()

        # prioritize mines if in first place
        if targets[0] == self.hero:
            if self.hero.life > 60:
                if self._dist_to_nearest_mine() < 10:
                    command = self._go_to_nearest_mine()
                else:
                    command = self._go_to_target_hero(targets[1])
            else:
                command = self._go_to_nearest_tavern()

        # prioritize killing the leader if not in first place
        else:
            if self.hero.life > 50:
                command = self._go_to_target_hero(targets[0])
            else:
                command = self._go_to_nearest_tavern()

        return command



    def _prioritize_bounties(self):
        """ chooses a player to hunt down based on value and distance"""
        x = self.hero.x
        y = self.hero.y

        for hero in self.game.heroes:
            hero.income   = float(hero.mine_count) / len(self.game.mines)
            hero.distance = vin.utils.distance_manhattan(x, y, hero.x, hero.y)
            hero.priority = hero.income - (0.3 * hero.distance) + (0.1 * hero.gold)


        priority_list = sorted(self.game.heroes, key = lambda p: p.priority, reverse = True)


        return priority_list


    def _go_to_target_hero(self, hero):
        command = self._go_to(hero.x, hero.y)

        if command:
            print("{0} hunting player {1}({2})".format(self.hero.name, hero.name, hero.id))
            return command
        else:
            return self._random


    def _dist_to_nearest_tavern(self):
        x = self.hero.x
        y = self.hero.y

        tavern = vin.utils.order_by_distance(x, y , self.game.taverns)[0]
        dist   = vin.utils.distance_manhattan(x, y, tavern.x, tavern.y)

        return dist


    def _go_to_nearest_tavern(self):
        x = self.hero.x
        y = self.hero.y

        # Order taverns by distance
        taverns = vin.utils.order_by_distance(x, y, self.game.taverns)
        for tavern in taverns:
            command = self._go_to(tavern.x, tavern.y)

            if command:
                print("{0} going to nearest tavern".format(self.hero.name))
                return command

        return self._random()


    def _dist_to_nearest_mine(self):
        x = self.hero.x
        y = self.hero.y

        mines = vin.utils.order_by_distance(x, y , self.game.mines)
        for mine in mines:
            if mine.owner != self.hero:
                return vin.utils.distance_manhattan(x, y, mine.x, mine.y)

        return 999


    def _go_to_nearest_mine(self):
        x = self.hero.x
        y = self.hero.y

        # Order mines by distance
        mines = vin.utils.order_by_distance(x, y, self.game.mines)
        for mine in mines:

            # Grab nearest mine that is not owned by this hero
            if mine.owner != self.hero.id:
                command = self._go_to(mine.x, mine.y)

                if command:
                    print("{0} going to nearest mine".format(self.hero.name))
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
        return random.choice(['North', 'West', 'East', 'South'])