# Testy jednostkowe dla metod klasy Game,
# która jest w pliku halma.py.
#
# Autor: Antoni Przybylik

import halma
from halma import state


# Metoda in_camp.
#
# Ta funkcja mówi, czy
# dane pole leży na planszy.


def test_in_camp1():
    game = halma.Game()

    assert game.in_camp(0, 0) == 'b'


def test_in_camp2():
    game = halma.Game()

    assert game.in_camp(1, 4) == 'b'


def test_in_camp3():
    game = halma.Game()

    assert game.in_camp(1, 5) == 'n'


def test_in_camp4():
    game = halma.Game()

    assert game.in_camp(15, 15) == 'w'


def test_in_camp5():
    game = halma.Game()

    assert game.in_camp(14, 14) == 'w'


def test_in_camp6():
    game = halma.Game()

    assert game.in_camp(8, 8) == 'n'


# Funkcja setup.
#
# Ta funkcja ustawia grę.


def test_setup_classic():
    game = halma.Game()
    game.setup('classic')

    # Dla każdego pola sprawdzamy, czy:
    #   czarny pionek <=> jest to obóz czarnego
    #   biały pionek <=> jest to obóz białego
    #   puste pole <=> nie jesteśmy w obozie
    for i in range(16):
        for j in range(16):
            if (game.in_camp(i, j) == 'w'):
                assert game._board[i][j] == state.WHITE

            if (game.in_camp(i, j) == 'b'):
                assert game._board[i][j] == state.BLACK

            if (game.in_camp(i, j) == 'n'):
                assert game._board[i][j] == state.EMPTY


# Metody set_field, read_field
#
# Za ich pomocą można ustawić
# lub odczytać stan pola na
# planszy.


def test_set_read1():
    game = halma.Game()

    game.set_field(10, 10, state.BLACK)
    assert game.read_field(10, 10) == state.BLACK


def test_set_read2():
    game = halma.Game()

    game.set_field(0, 0, state.WHITE)
    assert game.read_field(0, 0) == state.WHITE


# Metody save, load
#
# Za ich pomocą można zapisywać
# i wczytywać grę z pliku.


def test_save_load1():
    game = halma.Game()
    game.setup('random')
    game.save('/tmp/random_game.json')

    game2 = halma.Game()
    game2.load('/tmp/random_game.json')

    assert game.mode == game2.mode
    assert game.move == game2.move
    assert str(game._board) == str(game2._board)
