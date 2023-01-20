# Autor: Antoni Przybylik

from enum import Enum


class STATE(Enum):
    """! Stan pola planszy. """
    EMPTY = 1
    WHITE = 2
    BLACK = 3


class PLAYER(Enum):
    """! Gracz. """
    WHITE = 1
    BLACK = 2


class CAMP(Enum):
    """! Obóz. """
    WHITE = 1
    BLACK = 2
