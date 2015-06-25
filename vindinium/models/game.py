import vindinium as vin
from vindinium.models import Hero, Map, Tavern, Mine

__all__ = ['Game']


class Game(object):
    """ Represents a game.

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
        self.__processStartingState(state)


    def update(self, state, hero_id = None):
        """Updates the game with new information.

        Notice that, this function does not re-create the objects, just update
        the current objects with new information.

        Args:
            state (dict): the state object.
            hero_id int: the id of friendly hero
        """
        size = state['game']['board']['size']
        tiles = state['game']['board']['tiles']
        heroes = state['game']['heroes']

        # update the heroes
        for hero, hero_state in zip(self.heroes, heroes):
            hero.crashed    = hero_state['crashed']
            hero.mine_count = hero_state['mineCount']
            hero.gold       = hero_state['gold']
            hero.life       = hero_state['life']
            hero.last_dir   = hero_state.get('lastDir')
            hero.x          = hero_state['pos']['y']
            hero.y          = hero_state['pos']['x']

        # update the mines
        for mine in self.mines:
            char = tiles[mine.x * 2 + mine.y * 2 * size + 1]
            if char == "-":
                mine.owner = None
            else:
                mine.owner = int(char)

                board = state['game']['board']

        # set the map to empty and refill it with hero information
        for y in xrange(size):
            for x in xrange(size):

                self.map[x, y] = self.empty_map[x, y]

                for hero in self.heroes:

                    # logical checks
                    is_mine        = self.map[x, y] == vin.TILE_MINE
                    is_wall        = self.map[x, y] == vin.TILE_WALL
                    is_tavern      = self.map[x, y] == vin.TILE_TAVERN
                    is_spawn       = self.map[x, y] == vin.TILE_SPAWN

                    is_now_hero    = hero.x == x and hero.y == y
                    is_now_adj     = vin.utils.distance_manhattan(hero.x, hero.y, x, y) == 1
                    is_now_near    = vin.utils.distance_manhattan(hero.x, hero.y, x, y) == 2

                    if is_now_hero and is_spawn:
                        self.map[x, y] = vin.TILE_SPAWN_HERO
                    elif is_now_hero:
                        self.map[x, y] = vin.TILE_HERO

                    # only set adjacencies if they are about an enemy hero.
                    if hero_id is not None and hero.id != hero_id:
                        if is_now_adj and not any([is_mine, is_wall, is_tavern, is_spawn, is_now_hero]):
                            self.map[x, y] = vin.TILE_ADJ_HERO

                        if is_now_near and not any([is_mine, is_wall, is_tavern, is_spawn, is_now_hero, is_now_adj]):
                            self.map[x, y] = vin.TILE_NEAR_HERO



    def __processStartingState(self, state):
        """ Process the state for the FIRST time only."""
        # helper variables
        board = state['game']['board']
        size = board['size']
        tiles = board['tiles']
        tiles = [tiles[i:i + 2] for i in xrange(0, len(tiles), 2)]

        # run through the map and update map, mines and taverns
        self.map = Map(size)
        self.empty_map = Map(size)
        for y in xrange(size):
            for x in xrange(size):
                tile = tiles[y * size + x]
                if tile == '##':
                    self.map[x, y] = vin.TILE_WALL
                    self.empty_map[x, y] = vin.TILE_WALL

                elif tile == '[]':
                    self.map[x, y] = vin.TILE_TAVERN
                    self.empty_map[x, y] = vin.TILE_TAVERN
                    self.taverns.append(Tavern(x, y))

                elif tile.startswith('$'):
                    self.map[x, y] = vin.TILE_MINE
                    self.empty_map[x, y] = vin.TILE_MINE
                    self.mines.append(Mine(x, y))

                elif tile.startswith("@"):
                    self.map[x, y] = vin.TILE_HERO
                    self.empty_map[x, y] = vin.TILE_EMPTY

                else:
                    self.map[x, y] = vin.TILE_EMPTY
                    self.empty_map[x, y] = vin.TILE_EMPTY

        # create heroes
        for hero in state['game']['heroes']:

            pos = hero['spawnPos']

            self.empty_map[pos['y'], pos['x']] = vin.TILE_SPAWN

            # this is needed because sometimes heroes do not enter the match at their spawn points
            if self.map[pos['y'], pos['x']] == vin.TILE_HERO:
                self.map[pos['y'], pos['x']] = vin.TILE_SPAWN_HERO
            else:
                self.map[pos['y'], pos['x']] = vin.TILE_SPAWN

            self.heroes.append(Hero(hero))


