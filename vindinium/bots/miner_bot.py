import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import AStar

__all__ = ['MinerBot']


class MinerBot(BaseBot):
    """
    this bots primary objective is to mine. It avoids all
    other heros, and does not capture friendly bots mines.
    """
    
    search = None

    def start(self):
        self._update_pathfinding()


    def _update_pathfinding(self):
        ms = float(self.game.map.size)
        self.search = AStar(self.game.map, ms * 4, ms * 4, 5)


    def move(self):

        self._update_pathfinding()

        t, td = vin.utils.order_by_distance(self.hero.x, self.hero.y,
                                    self.game.taverns, self.game.map, self.search)

        if self.hero.life < 30:
            command = self._go_to_nearest_tavern()
        elif self.hero.life < 80 and td[0] < 2:
            command = self._go_to_nearest_tavern()
        else:
            command = self._go_to_nearest_mine()

        # send random command if hero has been still for 3+ turns
        if self.is_still(4):
            command = self._random()

        return command


    def _go_to_nearest_mine(self):
        x = self.hero.x
        y = self.hero.y

        command = None
        mines, dists = vin.utils.order_by_distance(x, y, self.game.mines,
                                    self.game.map, self.search, lim = len(self.game.mines))

        for i, mine in enumerate(mines):

            if not mine.friendly:
                command = self._go_to(mine.x, mine.y)
                return command

        return self._go_to_nearest_tavern()


    def _go_to_nearest_tavern(self):
        x = self.hero.x
        y = self.hero.y

        # Order taverns by distance
        taverns, dist = vin.utils.order_by_distance(x, y, self.game.taverns, self.game.map, self.search)
        for tavern in taverns:
            command = self._go_to(tavern.x, tavern.y)

            if command:
                return command

        return self._random()