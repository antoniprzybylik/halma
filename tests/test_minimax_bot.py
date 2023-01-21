# Testy bota MinimaxBot.
#
# Autor: Antoni Przybylik

from bots.minimax_bot import MinimaxBot
from halma.engine import Engine

from halma.defs import PLAYER
from halma.defs import STATE

import copy

# Metoda _state_quality.
#
# Ocenia jakość stanu gry.


def test_state_quality1():
    engine = Engine()
    engine.setup('classic')

    bot = MinimaxBot(PLAYER.WHITE, engine)
    assert bot._state_quality(engine._board) == 0


def test_state_quality2():
    engine = Engine()
    engine.setup('classic')
    engine.set_field(1, 1, STATE.WHITE)

    bot = MinimaxBot(PLAYER.WHITE, engine)
    assert bot._state_quality(engine._board) == 15


def test_state_quality3():
    engine = Engine()
    engine.setup('classic')
    engine.set_field(8, 8, STATE.WHITE)

    bot = MinimaxBot(PLAYER.WHITE, engine)
    assert bot._state_quality(engine._board) == 8


# Metody _move_on_board, _reverse_move_on_board.
#
# Pierwsza przemieszcza pionek na planszy, druga
# cofa ruch.


def test_move_reverse():
    engine = Engine()
    engine.setup('classic')

    board1 = copy.deepcopy(engine._board)
    board2 = copy.deepcopy(engine._board)

    bot = MinimaxBot(PLAYER.WHITE, engine)

    my_move = [(2, 2), (3, 3)]
    bot._move_on_board(board1, *my_move)
    bot._reverse_move_on_board(board1, *my_move)

    assert str(board1) == str(board2)
