# Testy bota AgressiveMinimaxBot.
#
# Autor: Antoni Przybylik

from bots.agressive_minimax_bot import AgressiveMinimaxBot
from halma.engine import Engine

from halma.defs import PLAYER

import copy


# Metody _move_on_board, _reverse_move_on_board.
#
# Pierwsza przemieszcza pionek na planszy, druga
# cofa ruch.


def test_move_reverse():
    engine = Engine()
    engine.setup('classic')

    board1 = copy.deepcopy(engine._board)
    board2 = copy.deepcopy(engine._board)

    bot = AgressiveMinimaxBot(PLAYER.WHITE, engine)

    my_move = [(2, 2), (3, 3)]
    bot._move_on_board(board1, *my_move)
    bot._reverse_move_on_board(board1, *my_move)

    assert str(board1) == str(board2)
