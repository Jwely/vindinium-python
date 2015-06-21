import vindinium as vin
from vindinium.models import Hero, Map, Tavern, Mine

__all__ = ['Game']


class Game(object):
    """Represents a game.

    A game object holds information about the game and is updated automatically
    by ``BaseBot``.

    Attributes:
        id (int): the game id.
        max_turns (int): maximum turns of the game (notice that each turn only
          a single hero moves).
        turn (int): current turn.
        map (vindinium.models.Map): a map instance.
        heroes (list): a list of Hero instances.
        mines (list): a list of Mine instances.
        taverns (list): a list of Tavern instances.
    """

    def __init__(self, state):
        """Constructor.

        Args:
            state (dict): the state object.
        """
        # Constants
        self.id = state['game']['id']
        self.max_turns = state['game']['maxTurns']
        
        # Variables
        self.turn = state['game']['turn']

        # Processed objects
        self.map = None
        self.heroes = []
        self.mines = []
        self.taverns = []

        # Process the state, creating the objects
        self.__processState(state)


    def update(self, state):
        """Updates the game with new information.

        Notice that, this function does not re-create the objects, just update
        the current objects with new information.

        Args:
            state (dict): the state object.
        """
        size = state['game']['board']['size']
        tiles = state['game']['board']['tiles']
        heroes = state['game']['heroes']
        
        for hero, hero_state in zip(self.heroes, heroes):
            hero.crashed    = hero_state['crashed']
            hero.mine_count = hero_state['mineCount']
            hero.gold       = hero_state['gold']
            hero.life       = hero_state['life']
            hero.last_dir   = hero_state.get('lastDir')
            hero.x          = hero_state['pos']['y']
            hero.y          = hero_state['pos']['x']

        for mine in self.mines:
            char = tiles[mine.x * 2 + mine.y * 2 * size + 1]
            if char == "-":
                mine.owner = None
            else:
                mine.owner = int(char)

        self.__processStateAgain(state)


    def __processState(self, state):
        """Process the state for the FIRST time"""
        # helper variables
        board = state['game']['board']
        size = board['size']
        tiles = board['tiles']
        tiles = [tiles[i:i + 2] for i in xrange(0, len(tiles), 2)]

        # run through the map and update map, mines and taverns
        self.map = Map(size)
        for y in xrange(size):
            for x in xrange(size):
                tile = tiles[y * size + x]
                if tile == '##':
                    self.map[x, y] = vin.TILE_WALL

                elif tile == '[]':
                    self.map[x, y] = vin.TILE_TAVERN
                    self.taverns.append(Tavern(x, y))

                elif tile.startswith('$'):
                    self.map[x, y] = vin.TILE_MINE
                    self.mines.append(Mine(x, y))

                elif tile.startswith("@"):
                    self.map[x, y] = vin.TILE_HERO

                else:
                    self.map[x, y] = vin.TILE_EMPTY

        # create heroes
        for hero in state['game']['heroes']:

            pos = hero['spawnPos']

            # this is needed because sometimes heroes do not enter the match at their spawn points
            if self.map[pos['y'], pos['x']] == vin.TILE_HERO:
                self.map[pos['y'], pos['x']] = vin.TILE_SPAWN_HERO
            else:
                self.map[pos['y'], pos['x']] = vin.TILE_SPAWN

            self.heroes.append(Hero(hero))


    def __processStateAgain(self, state):
        """ update the map state with the dynamic components"""
        # helper variables
        board = state['game']['board']
        size = board['size']
        tiles = board['tiles']
        tiles = [tiles[i:i + 2] for i in xrange(0, len(tiles), 2)]

        # update tiles that might have changed, empties and heroes
        for y in xrange(size):
            for x in xrange(size):
                tile = tiles[y * size + x]
                if tile.startswith("@"):

                    if self.map[x, y] == vin.TILE_SPAWN or self.map[x, y] == vin.TILE_SPAWN_HERO:
                        self.map[x, y] = vin.TILE_SPAWN_HERO
                    else:
                        self.map[x, y] = vin.TILE_HERO

                elif tile == "  ":
                    if self.map[x, y] != vin.TILE_SPAWN and self.map[x, y] != vin.TILE_SPAWN_HERO:
                        self.map[x, y] = vin.TILE_EMPTY
                    else:
                        self.map[x, y] = vin.TILE_SPAWN

        # set hero adjacency locations
        for y in xrange(size):
            for x in xrange(size):
                tile = tiles[y * size + x]

                if tile.startswith("@"):

                    adj_list = [(x + 1, y),
                                (x - 1, y),
                                (x, y + 1),
                                (x, y - 1)]

                    for adj in adj_list:
                        try:
                            # several lengthy conditions
                            empty = self.map[adj[0], adj[1]] == vin.TILE_EMPTY
                            spawn = self.map[adj[0], adj[1]] == vin.TILE_SPAWN
                            sphro = self.map[adj[0], adj[1]] == vin.TILE_SPAWN_HERO
                            if empty and not spawn and not sphro:
                                self.map[adj[0], adj[1]] = vin.TILE_ADJ_HERO
                        except IndexError:
                            pass


