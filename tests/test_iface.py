# Testy jednostkowe dla metod klasy
# GameInterface znajdującej się w pliku
# halma/iface.py
#
# Autor: Antoni Przybylik

from halma.game import Game
from halma.iface import GameInterface

from halma.defs import STATE

# Metoda in_camp.
#
# Ta funkcja mówi, czy
# dane pole leży na planszy.


def test_in_camp1():
    game = Game()
    game_iface = GameInterface(game)

    assert game_iface.in_camp(0, 0) == 'b'


def test_in_camp2():
    game = Game()
    game_iface = GameInterface(game)

    assert game_iface.in_camp(1, 4) == 'b'


def test_in_camp3():
    game = Game()
    game_iface = GameInterface(game)

    assert game_iface.in_camp(1, 5) == 'n'


def test_in_camp4():
    game = Game()
    game_iface = GameInterface(game)

    assert game_iface.in_camp(15, 15) == 'w'


def test_in_camp5():
    game = Game()
    game_iface = GameInterface(game)

    assert game_iface.in_camp(14, 14) == 'w'


def test_in_camp6():
    game = Game()
    game_iface = GameInterface(game)

    assert game_iface.in_camp(8, 8) == 'n'


# Metoda setup.
#
# Ta funkcja ustawia grę.


def test_setup_classic():
    game = Game()
    game_iface = GameInterface(game)
    game_iface.setup('classic')

    board = game_iface.get_board()

    # Dla każdego pola sprawdzamy, czy:
    #   czarny pionek <=> jest to obóz czarnego
    #   biały pionek <=> jest to obóz białego
    #   puste pole <=> nie jesteśmy w obozie
    for i in range(16):
        for j in range(16):
            if (game_iface.in_camp(i, j) == 'w'):
                assert board[i][j] == STATE.WHITE

            if (game_iface.in_camp(i, j) == 'b'):
                assert board[i][j] == STATE.BLACK

            if (game_iface.in_camp(i, j) == 'n'):
                assert board[i][j] == STATE.EMPTY


# Metoda move.
#
# Ta funkcja wykonuje ruch.

def test_move1():
    game = Game()
    game_iface = GameInterface(game)

    game.set_field(1, 1, STATE.WHITE)
    game.set_field(2, 1, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bb-cc') is True


def test_move2():
    game = Game()
    game_iface = GameInterface(game)

    game.set_field(1, 1, STATE.WHITE)
    game.set_field(2, 1, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bb-bc') is True


def test_move3():
    game = Game()
    game_iface = GameInterface(game)

    game.set_field(1, 1, STATE.WHITE)
    game.set_field(2, 1, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bb-cb') is False


def test_move4():
    game = Game()
    game_iface = GameInterface(game)

    game.set_field(1, 1, STATE.WHITE)
    game.set_field(2, 1, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bb-ac') is True


def test_move5():
    game = Game()
    game_iface = GameInterface(game)

    game.set_field(1, 3, STATE.WHITE)
    game.set_field(2, 5, STATE.BLACK)
    game.set_field(3, 4, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bd-ce') is True


def test_move6():
    game = Game()
    game_iface = GameInterface(game)

    game.set_field(1, 0, STATE.BLACK)
    game.set_field(0, 3, STATE.BLACK)
    game.set_field(1, 2, STATE.WHITE)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bc-ac') is True
