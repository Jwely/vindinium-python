"""Awesome python client for Vindinium.

Vindinium is an online and continuous competition where you control a bot in a
turn-based game, consult `the site <http://vindinium.org>`_ to know more.
Note: this client is based on the `ornicar's client
<https://github.com/ornicar/vindinium-starter-python>`_.

This library provides several base and simple bots, helper structures and
common algorithms that allow you to create bots in an easy and fast way,
focusing on the strategy and specific techniques of your bot.

The library has the following features:

- Bots:
    - RawBot: a bot that does nothing.
    - BaseBot: a bot that process the state and create and update a Game object.
    - RandomBot: a bot that perform random movements.
    - MinerBot: a bot that looks for mines continuously.

- Models (used by base bot to create the game structure):
    - Game: stores all other models.
    - Map: stores static information about the map.
    - Mine: represents a mine in the map.
    - Hero: represents a hero in the game.
    - Tavern: represents a tavern in the game.

- AI algorithms (in general, already specialized for vindinium):
    - AStar: the A* algorithm.

Note: this client fix the inconsistent axis of the server, so you don't have to
worry about that (if you're using the game model).

"""

from .client import *
from . import bots
from . import models
from . import ai
from . import utils

# CONSTANTS
# tile values
TILE_EMPTY      = 0     # space that may be freely moved through
TILE_WALL       = 1     # a total blockage
TILE_SPAWN      = 2     # any spawn location
TILE_TAVERN     = 3     # any tavern location
TILE_MINE       = 4     # any mine location
TILE_HERO       = 5     # any hero location
TILE_ADJ_HERO   = 6     # when a tile is adjacent to a hero (one move away)
TILE_NEAR_HERO  = 7     # when a tile is adjacent to a hero adjacent tile (two moves away)
TILE_SPAWN_HERO = 8     # when a hero and a spawn location are coincident

# command values
NORTH = 'North'
SOUTH = 'South'
WEST  = 'West'
EAST  = 'East'
STAY  = 'Stay'

# direction
DIR_NORTH = (-1, 0)
DIR_SOUTH = (1, 0)
DIR_WEST  = (0, -1)
DIR_EAST  = (0, 1)
DIR_STAY  = (0, 0)

# adjacency list
DIR_NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# friendly bot list
FRIENDLY = ["jbot01", "jbot02", "jbot03", "jbot04", "jbot05", "jwely"]