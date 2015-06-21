__all__ = ['Map']

import vindinium as vin

class Map(object):
    """Represents static elements in the game, such as walls, paths, taverns,
    mines and spawn points.

    Attributes:
        size (int): the board size (in a single axis).
    """
    
    def __init__(self, size):
        """Constructor.

        Args:
            size (int): the board size.
        """
        self.size = size
        self.__board = [[0 for i in xrange(size)] for j in xrange(size)]

    def __getitem__(self, key):
        """Returns an item in the map."""
        return self.__board[key[0]][key[1]]

    def __setitem__(self, key, value):
        """Sets an item in the map."""
        self.__board[key[0]][key[1]] = value

    def __str__(self, heroes = None):
        """ Pretty map. input heroes for hero IDs to print to the map"""
        s = ' '
        s += '---' * self.size + '\n'
        for y in xrange(self.size):
            s += '|'
            for x in xrange(self.size):
                if self[x, y]:

                    if self[x, y] == vin.TILE_WALL:
                        s += "<#>"

                    elif self[x, y] == vin.TILE_TAVERN:
                        s += " t "

                    elif self[x, y] == vin.TILE_MINE:
                        s += " $ "

                    elif self[x, y] == vin.TILE_SPAWN:
                        s += " : "

                    elif self[x, y] == vin.TILE_HERO:
                        if heroes is not None:
                            for hero in heroes:
                                if hero.x == x and hero.y == y:
                                    s += "({0})".format(hero.id)
                        else:
                            s += "(0)"

                    elif self[x, y] == vin.TILE_ADJ_HERO:
                        s += " ~ "

                # blank spaces
                else:
                    s += "   "

            s += '|\n'
        s += ' ' + '---'*(self.size)
        return s