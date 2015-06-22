import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import AStar

__all__ = ['MinerBot']


class MinerBot(BaseBot):
    """ this bots primary objective is to mine , it avoids enemy heroes"""
    
    search = None

    def start(self):
        self._update_pathfinding()


    def _update_pathfinding(self):
        ms = float(self.game.map.size)
        self.search = AStar(self.game.map, ms / 2 , 3)


    def move(self):

        self._update_pathfinding()

        if self.hero.life < 50:
            command = self._go_to_nearest_tavern()
        else:
            command =  self._go_to_nearest_mine()

        self._log_brainwave(command, map = True)
        return command


    def _go_to_nearest_mine(self):
        x = self.hero.x
        y = self.hero.y

        # Order mines by distance
        mines, dists = vin.utils.order_by_distance(x, y, self.game.mines, self.game.map, self.search)

        for i, mine in enumerate(mines):

            # Grab nearest mine that is not owned by this hero
            if mine.owner != self.hero.id:
                command = self._go_to(mine.x, mine.y)

                if command:
                    return command

        # if no mines could be navigated to, just go to the nearest tavern
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