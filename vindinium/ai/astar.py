import vindinium as vin
from vindinium.ai import HeapQueue

__all__ = ['AStar']

DIR_NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class AStar(object):
    """A* algorithm specialized for vindinium.

    The A* algorithm receives an instance of ``vindinium.models.Map``` and  
    compute the best path when necessary. 

    Attributes:
        cost_avoid (float):     cost to walk over an avoidable tile (consult the
                                    avoid_tiles attribute). Defaults to 4.
        cost_move (float):      cost to walk over an empty tile. Defaults to 1.
        obstacle_tiles (list):  a list of obstacles tile VALUES.
        avoid_tiles (list):     a list of avoidable tile VALUES.
    """

    def __init__(self, game_map, cost_adj = 8, cost_near = 6, cost_spawn = 4):
        """Constructor.

        Args:
            map (vindinium.models.Map): the map instance.
            cost_avoid_hero:   acceptable cost of avoiding a hero occupied tile
            cost_avoid:        acceptable cost of avoiding an avoid tile (spawns)

            costs input is as follows [avoid_adjacency, avoid_nearness, avoid_spawn_points]
        """

        self.cost_avoid_adj   = cost_adj
        self.cost_avoid_near  = cost_near
        self.cost_avoid_spawn = cost_spawn
        self.cost_move = 1


        self.obstacle_tiles = [vin.TILE_WALL, vin.TILE_TAVERN, vin.TILE_MINE]
        self.avoid_spawn    = [vin.TILE_SPAWN]
        self.avoid_adj      = [vin.TILE_ADJ_HERO, vin.TILE_HERO, vin.TILE_SPAWN_HERO]
        self.avoid_near     = [vin.TILE_NEAR_HERO]

        self._map = game_map


    def find(self, x0, y0, x1, y1):
        """Find a path between (x0, y0) and (x1, y1).

        Args:
            x0 (int): initial position in X.
            y0 (int): initial position in Y.
            x1 (int): goal position in X.
            y1 (int): goal position in Y.

        Returns:
            (list) if the path has been found, e.g. ``[(0, 1), (0, 2), ...]``.
              Notice that, it does not include the initial position, but
              include the goal.
            (None) otherwise.
        """

        # To avoid access on the dot
        game_map = self._map
        adjacent = False

        # If obstacle, cancel search
        if game_map[x1, y1] in self.obstacle_tiles:
            adjacent = True

        # State x, y, g, parent
        start = (x0, y0, 0, None)
        queue = HeapQueue()
        visited = [(x0, y0)]
        
        queue.push(start, 0)
        while not queue.is_empty():
            state = queue.pop()
            x, y, g, parent = state

            # Goal
            if (x == x1 and y == y1) or (adjacent and (abs(x - x1) + abs(y - y1)) == 1):
                break

            # Children
            for x_, y_ in self.__neighbors(x, y, visited):
                tile = game_map[x_, y_]

                # determine cost based on tile type
                if tile in self.avoid_spawn:
                    cost = self.cost_avoid_spawn

                elif tile in self.avoid_adj:
                    cost = self.cost_avoid_adj

                elif tile in self.avoid_near:
                    cost = self.cost_avoid_near

                else:
                    cost = self.cost_move

                g_ = g + cost
                h_ = abs(x_ - x1) + abs(y_ - y1)
                queue.push((x_, y_, g_, state), g_ + h_)

        # If while does not break, no path was discovered.
        else:
            return None

        # Prepare result
        result = []
        while state:
            result.insert(0, (state[0], state[1]))
            state = state[3]
        result.pop(0)

        return result


    def __neighbors(self, x, y, visited):
        """Get the valid neighbors of a tile."""
        m = self._map
        s = m.size
        for dx, dy in DIR_NEIGHBORS:
            tx, ty = x + dx, y + dy
            
            if not(-1 < tx < s and -1 < ty < s):
                continue

            tile = m[tx, ty]
            if tile not in self.obstacle_tiles and (tx, ty) not in visited:
                visited.append((tx, ty))
                yield tx, ty
