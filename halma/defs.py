# Autor: Antoni Przybylik

from enum import Enum


class state(Enum):
    """! Stan pola planszy. """
    EMPTY = 1
    WHITE = 2
    BLACK = 3


class player(Enum):
    """! Gracz. """
    WHITE = 1
    BLACK = 2
