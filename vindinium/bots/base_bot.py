from vindinium.bots import RawBot
from vindinium.models import Game

__all__ = ['BaseBot']


class BaseBot(RawBot):
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


    def _log_brainwave(self, thought):
        """ attaches a printout of the map state to the brainwave log """
        brainwave = (thought, self.game.map.__str__(self.game.heroes))
        self.brainwaves.append(brainwave)
        print("{0} \n {1}".format(brainwave[0], brainwave[1]))


    def _start(self, state):
        """ Wrapper to start method """
        self.id = state['hero']['id']
        self.state = state
        self.game = Game(state)
        self.hero = self.game.heroes[self.id - 1]
        self.brainwaves = []
        self.start()


    def _move(self, state):
        """ Wrapper to move method."""
        self.state = state
        self.game.update(state)
        return self.move()


    def _end(self):
        """ Wrapper to end method."""
        self.end()