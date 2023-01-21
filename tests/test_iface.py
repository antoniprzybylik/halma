# Testy jednostkowe dla metod klasy
# GameInterface znajdującej się w pliku
# halma/iface.py
#
# Autor: Antoni Przybylik

from halma.engine import Engine
from halma.iface import GameInterface

from halma.defs import STATE
from halma.defs import CAMP
from halma.defs import PLAYER

# Metoda in_camp.
#
# Ta funkcja mówi, czy
# dane pole leży na planszy.


def test_in_camp1():
    engine = Engine()
    game_iface = GameInterface(engine)

    assert game_iface.in_camp(0, 0) == CAMP.BLACK


def test_in_camp2():
    engine = Engine()
    game_iface = GameInterface(engine)

    assert game_iface.in_camp(1, 4) == CAMP.BLACK


def test_in_camp3():
    engine = Engine()
    game_iface = GameInterface(engine)

    assert game_iface.in_camp(1, 5) is None


def test_in_camp4():
    engine = Engine()
    game_iface = GameInterface(engine)

    assert game_iface.in_camp(15, 15) == CAMP.WHITE


def test_in_camp5():
    engine = Engine()
    game_iface = GameInterface(engine)

    assert game_iface.in_camp(14, 14) == CAMP.WHITE


def test_in_camp6():
    engine = Engine()
    game_iface = GameInterface(engine)

    assert game_iface.in_camp(8, 8) is None


# Metoda setup.
#
# Ta funkcja ustawia grę.


def test_setup_classic():
    engine = Engine()
    game_iface = GameInterface(engine)
    game_iface.setup('classic')

    board = game_iface.get_board()

    # Dla każdego pola sprawdzamy, czy:
    #   czarny pionek <=> jest to obóz czarnego
    #   biały pionek <=> jest to obóz białego
    #   puste pole <=> nie jesteśmy w obozie
    for i in range(16):
        for j in range(16):
            if (game_iface.in_camp(i, j) == CAMP.WHITE):
                assert board[i][j] == STATE.WHITE

            if (game_iface.in_camp(i, j) == CAMP.BLACK):
                assert board[i][j] == STATE.BLACK

            if (game_iface.in_camp(i, j) is None):
                assert board[i][j] == STATE.EMPTY


# Metoda move.
#
# Ta funkcja wykonuje ruch.

def test_move1():
    engine = Engine()
    game_iface = GameInterface(engine)

    engine.set_field(1, 1, STATE.WHITE)
    engine.set_field(2, 1, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bb-cc') is not None


def test_move2():
    engine = Engine()
    game_iface = GameInterface(engine)

    engine.set_field(1, 1, STATE.WHITE)
    engine.set_field(2, 1, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bb-bc') is not None


def test_move3():
    engine = Engine()
    game_iface = GameInterface(engine)

    engine.set_field(1, 1, STATE.WHITE)
    engine.set_field(2, 1, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bb-cb') is None


def test_move4():
    engine = Engine()
    game_iface = GameInterface(engine)

    engine.set_field(1, 1, STATE.WHITE)
    engine.set_field(2, 1, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bb-ac') is not None


def test_move5():
    engine = Engine()
    game_iface = GameInterface(engine)

    engine.set_field(1, 3, STATE.WHITE)
    engine.set_field(2, 5, STATE.BLACK)
    engine.set_field(3, 4, STATE.BLACK)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bd-ce') is not None


def test_move6():
    engine = Engine()
    game_iface = GameInterface(engine)

    engine.set_field(1, 0, STATE.BLACK)
    engine.set_field(0, 3, STATE.BLACK)
    engine.set_field(1, 2, STATE.WHITE)

    # Czy uda się wykonać ruch.
    assert game_iface.move('bc-ac') is not None

# Metoda get_winner.
#
# Ta funkcja sprawdza, czy
# któryś gracz ma sytuację
# wygrywającą i jeśli tak jest
# zwraca który to gracz.


def test_winner1():
    engine = Engine()
    game_iface = GameInterface(engine)
    game_iface.setup('classic')

    assert game_iface.get_winner() is None


def test_winner2():
    engine = Engine()
    game_iface = GameInterface(engine)
    game_iface.setup('classic')

    engine.set_field(0, 0, STATE.WHITE)
    engine.set_field(1, 2, STATE.WHITE)

    assert game_iface.get_winner() == PLAYER.WHITE


def test_winner3():
    engine = Engine()
    game_iface = GameInterface(engine)
    game_iface.setup('classic')

    engine.set_field(14, 15, STATE.BLACK)
    engine.set_field(13, 13, STATE.BLACK)

    assert game_iface.get_winner() is PLAYER.BLACK


def test_winner4():
    engine = Engine()
    game_iface = GameInterface(engine)
    game_iface.setup('classic')

    engine.set_field(14, 15, STATE.BLACK)
    engine.set_field(13, 13, STATE.BLACK)
    engine.set_field(15, 14, STATE.EMPTY)

    assert game_iface.get_winner() is None


def test_winner5():
    engine = Engine()
    game_iface = GameInterface(engine)
    game_iface.setup('classic')

    engine.set_field(0, 0, STATE.WHITE)
    engine.set_field(1, 2, STATE.WHITE)
    engine.set_field(2, 2, STATE.EMPTY)

    assert game_iface.get_winner() is None
