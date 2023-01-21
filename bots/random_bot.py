# Bot wykonujący losowe ruchy.
#
# Autor: Antoni Przybylik

from halma.defs import STATE
from halma.defs import PLAYER

from bots.generic import GameBot

import random


class RandomBot(GameBot):
    """! Bot wykonujący losowe ruchy. """

    def make_move(self):
        """! Wykonuje ruch.

        @return Wykonany ruch.
        """

        board = self._engine.get_board()
        moving_player = self._engine.moving_player

        my_positions = []
        moves_to_consider = []

        for i in range(0, 16):
            for j in range(0, 16):
                field = board[i][j]

                if ((field == STATE.BLACK and
                     moving_player == PLAYER.BLACK) or
                    (field == STATE.WHITE and
                     moving_player == PLAYER.WHITE)):
                    my_positions.append((i, j))

        for pos_from in my_positions:
            for pos_to in self._engine.moves(pos_from[0], pos_from[1]):
                moves_to_consider.append((pos_from, pos_to))

        move = random.choice(moves_to_consider)
        self._apply_move(*move)

        return move
