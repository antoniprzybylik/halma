# Testy jednostkowe dla metod klasy Game,
# która jest w pliku halma.py.
#
# Autor: Antoni Przybylik

from pytest import raises

from halma.game import Game
from halma.game import state


# Metody set_field, read_field
#
# Za ich pomocą można ustawić
# lub odczytać stan pola na
# planszy.


def test_set_read1():
    game = Game()

    game.set_field(10, 10, state.BLACK)
    assert game.read_field(10, 10) == state.BLACK


def test_set_read2():
    game = Game()

    game.set_field(0, 0, state.WHITE)
    assert game.read_field(0, 0) == state.WHITE


# Metody save, load
#
# Za ich pomocą można zapisywać
# i wczytywać grę z pliku.


def test_save_load1():
    game = Game()
    game.setup('random')
    game.save('/tmp/random_game.json')

    game2 = Game()
    game2.load('/tmp/random_game.json')

    assert game.mode == game2.mode
    assert game.move == game2.move
    assert str(game._board) == str(game2._board)


def test_save_load2():
    with open('/tmp/broken_file.json', 'w') as fp:
        fp.write('{"mode": "classic", "move": "aalmakota"}')

    with raises(ValueError):
        game = Game()
        game.load('/tmp/broken_file.json')
