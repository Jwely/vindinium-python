__all__ = ['Tavern']


class Tavern(object):
    """A tavern.

    Attributes:
        x (int): the tavern position in X.
        y (int): the tavern position in Y.
    """

    def __init__(self, x, y):
        """Constructor

        Args:
            x (int): the mine position in X.
            y (int): the mine position in Y.
        """
        self.x = x
        self.y = y