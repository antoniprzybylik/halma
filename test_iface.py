# Testy jednostkowe dla metod klasy
# GameInterface znajdującej się w pliku
# iface.py
#
# Autor: Antoni Przybylik

import halma
from halma import state
import iface

# Metoda in_camp.
#
# Ta funkcja mówi, czy
# dane pole leży na planszy.


def test_in_camp1():
    game = halma.Game()
    game_iface = iface.GameInterface(game)

    assert game_iface.in_camp(0, 0) == 'b'


def test_in_camp2():
    game = halma.Game()
    game_iface = iface.GameInterface(game)

    assert game_iface.in_camp(1, 4) == 'b'


def test_in_camp3():
    game = halma.Game()
    game_iface = iface.GameInterface(game)

    assert game_iface.in_camp(1, 5) == 'n'


def test_in_camp4():
    game = halma.Game()
    game_iface = iface.GameInterface(game)

    assert game_iface.in_camp(15, 15) == 'w'


def test_in_camp5():
    game = halma.Game()
    game_iface = iface.GameInterface(game)

    assert game_iface.in_camp(14, 14) == 'w'


def test_in_camp6():
    game = halma.Game()
    game_iface = iface.GameInterface(game)

    assert game_iface.in_camp(8, 8) == 'n'


# Metoda setup.
#
# Ta funkcja ustawia grę.


def test_setup_classic():
    game = halma.Game()
    game_iface = iface.GameInterface(game)
    game_iface.setup('classic')

    board = game_iface.get_board()

    # Dla każdego pola sprawdzamy, czy:
    #   czarny pionek <=> jest to obóz czarnego
    #   biały pionek <=> jest to obóz białego
    #   puste pole <=> nie jesteśmy w obozie
    for i in range(16):
        for j in range(16):
            if (game_iface.in_camp(i, j) == 'w'):
                assert board[i][j] == state.WHITE

            if (game_iface.in_camp(i, j) == 'b'):
                assert board[i][j] == state.BLACK

            if (game_iface.in_camp(i, j) == 'n'):
                assert board[i][j] == state.EMPTY
