import vindinium as vin
from vindinium.models import Game
import random

__all__ = ['BaseBot']


class BaseBot():
    """ Base bot.

    Attributes:
        id (int): the bot's id.
        game (vindinium.models.Game): the game instance, updated by this object.
        hero (vindinium.models.Hero): the bot's hero instance, updated by this 
          object.
        state (dict): the unprocessed state from server.
    """

    id = None
    state = None
    game = None
    hero = None


    def start(self):
        return


    def move(self):
        return self._random


    def end(self):
        print("==== Final scores ====")
        for hero in self.game.heroes:
            print("{0} {1}".format(hero.name.ljust(15), hero.gold))
        return

    def is_still(self, num_turns):
        """
        returns True if hero has been still for num_turns turns
        """
        return False


    def _start(self, state):
        """ Wrapper to start method, called by client """
        self.id = state['hero']['id']
        self.state = state
        self.game = Game(state)
        self.hero = self.game.heroes[self.id - 1]

        print("I am {0}".format(self.hero.name))
        self.start()


    def _move(self, state):
        """ Wrapper to move method, called by client """
        self.state = state
        self.game.update(state, self.hero.id)
        return self.move()


    def _end(self):
        """ Wrapper to end method, called by client """
        self.end()


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