import vindinium
from vindinium.ai import AStar

__all__ = ['dir_to_command',
           'command_to_dir',
           'path_to_command',
           'distance_manhattan',
           'order_by_distance']


def dir_to_command(dx, dy):
    """ Converts a direction to a command.
    
    Args:
        dx (int): direction in X axis, must be 1, 0 or -1.
        dy (int): direction in Y axis, must be 1, 0 or -1.

    Returns:
        (string) a command.

    Raise:
        ValueError if direction is invalid.
    """
    if   dx == -1 and dy ==  0:
        return vindinium.WEST

    elif dx ==  1 and dy ==  0:
        return vindinium.EAST

    elif dx ==  0 and dy == -1:
        return vindinium.NORTH

    elif dx ==  0 and dy ==  1:
        return vindinium.SOUTH

    elif dx ==  0 and dy ==  0:
        return vindinium.STAY

    raise ValueError('Invalid direction (%s, %s).' % (dx, dy))


def command_to_dir(command):
    """Converts a command to a direction.

    Args:
        (string) the command.

    Returns:
        (tuple) a tuple (dx, dy) with the direction.

    Raise:
        ValueError if command is invalid.
    """
    if   command == vindinium.NORTH:
        return vindinium.DIR_NORTH

    elif command == vindinium.SOUTH:
        return vindinium.DIR_SOUTH

    elif command == vindinium.WEST:
        return vindinium.DIR_WEST

    elif command == vindinium.EAST:
        return vindinium.DIR_EAST

    elif command == vindinium.STAY:
        return vindinium.DIR_STAY

    raise ValueError('Invalid command "%s".' % command)


def path_to_command(x0, y0, x1, y1):
    """Converts an adjacent to a command.

    Args:
        x0 (int): initial position in X axis.
        y0 (int): initial position in Y axis.
        x1 (int): final position in X axis.
        y1 (int): final position in Y axis.

    Returns:
        (string) a command.

    Raise:
        ValueError if direction is invalid.
    """
    dx = x1 - x0
    dy = y1 - y0
    return dir_to_command(dx, dy)


def distance_manhattan(x0, y0, x1, y1):
    """Computes the manhattan distance between two points.

    Args:
        x0 (int): initial position in X axis.
        y0 (int): initial position in Y axis.
        x1 (int): final position in X axis.
        y1 (int): final position in Y axis.

    Returns
        (int) the distance.
    """
    return abs(x0 - x1) + abs(y0 - y1)


def distance_path(x0, y0, x1, y1, game_map, searcher = None):
    """
    finds preference weighted path distance between two points for a given game map and
    AStar pathfinding instance.
    """
    if searcher is None:
        searcher = AStar(game_map)

    return len(searcher.find(x0, y0, x1, y1))


def order_by_distance(x0, y0, objects, game_map = None, searcher = None):
    """ orders a list of objects by distance from input x0 and y0.

    if a game map and AStar AI pathfinder instance are provided, the distances
    will be according to the pathfinder which accounts for obstacles, current
    player positions, and avoidance preferences. if a game_map and searcher are
    not provided this function returns the simple manhattan distance.
    """
    if game_map is None:
        distances = [distance_manhattan(x0, y0, obj.x, obj.y) for obj in objects]
    else:
        distances = [distance_path(x0, y0, obj.x, obj.y, game_map, searcher) for obj in objects]

        distances, objects = zip(*sorted(zip(distances, objects)))
        return objects, distances





