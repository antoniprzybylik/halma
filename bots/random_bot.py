# Bot wykonujący losowe ruchy.
#
# Autor: Antoni Przybylik

from halma.game import state
from halma.game import player
from bots.generic import GameBot

import random


class RandomBot(GameBot):
    """! Bot wykonujący losowe ruchy. """

    def make_move(self):
        """! Wykonuje ruch. """

        board = self._game.get_board()
        moving_player = self._game.moving_player

        my_positions = []
        moves_to_consider = []

        for i in range(0, 16):
            for j in range(0, 16):
                field = board[i][j]

                if ((field == state.BLACK and
                     moving_player == player.BLACK) or
                    (field == state.WHITE and
                     moving_player == player.WHITE)):
                    my_positions.append((i, j))

        for pos_from in my_positions:
            for pos_to in self._game.moves(pos_from[0], pos_from[1]):
                moves_to_consider.append((pos_from, pos_to))

        self._apply_move(*random.choice(moves_to_consider))