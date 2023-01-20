# Testy jednostkowe dla metod
# klasy Game z pliku halma/game.py
#
# Autor: Antoni Przybylik

# Metody save, load
#
# Za ich pomocą można zapisywać
# i wczytywać grę z pliku.

from pytest import raises

from halma.engine import Engine
from halma.iface import GameInterface
from halma.game import Game

from halma.defs import PLAYER
from bots.random_bot import RandomBot


def test_save_load1():
    e = Engine()
    i = GameInterface(e)
    e.setup('random')
    p1, p2 = RandomBot(PLAYER.WHITE, e), RandomBot(PLAYER.BLACK, e)
    game = Game(e, i, p1, p2)
    game.save('/tmp/random_game.json')

    e2 = Engine()
    i2 = GameInterface(e2)
    game2 = Game(e2, i2)
    game2.load('/tmp/random_game.json')

    assert i.current_move() == i2.current_move()
    assert i.moving_player() == i2.moving_player()
    assert str(e._board) == str(e2._board)


def test_save_load2():
    with open('/tmp/broken_file.json', 'w') as fp:
        fp.write('{"mode": "classic", "move": "aalmakota"}')

    with raises(ValueError):
        e = Engine()
        i = GameInterface(e)
        game = Game(e, i)
        game.load('/tmp/broken_file.json')
