# Testy jednostkowe dla metod klasy Engine,
# która jest w pliku halma/engine.py.
#
# Autor: Antoni Przybylik

from halma.engine import Engine
from halma.iface import GameInterface
from halma.defs import STATE

import json


# Metody set_field, read_field
#
# Za ich pomocą można ustawić
# lub odczytać stan pola na
# planszy.


def test_set_read1():
    engine = Engine()

    engine.set_field(10, 10, STATE.BLACK)
    assert engine.read_field(10, 10) == STATE.BLACK


def test_set_read2():
    engine = Engine()

    engine.set_field(0, 0, STATE.WHITE)
    assert engine.read_field(0, 0) == STATE.WHITE


# Metody dump_state i load_state.
#
# Za ich pomocą można zapisać stan
# silnika w słowniku i wczytać stan
# silnika ze słownika.
#
# Zapisane stany silnika do użycia
# przy testowaniu są w katalogu
# rc (resources).

def test_dump_load1():
    with open('rc/engine_state1.json') as fp:
        state1 = json.load(fp)

    engine = Engine()
    engine.load_state(state1)

    state2 = engine.dump_state()
    assert str(state1) == str(state2)


def test_dump_load2():
    with open('rc/engine_state2.json') as fp:
        state1 = json.load(fp)

    engine = Engine()
    engine.load_state(state1)

    state2 = engine.dump_state()
    assert str(state1) == str(state2)


# TODO: Test broken state.

# Metoda moves.
#
# Zwraca wszystkie ruchy jakie możemy
# wykonać z danego pola.


possible_moves1 = [(3, 3), (2, 4), (4, 2)]


def test_moves1():
    engine = Engine()
    game_iface = GameInterface(engine)
    game_iface.setup('classic')

    possible_moves = engine.moves(2, 2)

    assert len(possible_moves) == len(possible_moves1)
    for pos in possible_moves:
        assert pos in possible_moves1


possible_moves2 = [(0, 5), (1, 5), (2, 4)]


def test_moves2():
    engine = Engine()
    game_iface = GameInterface(engine)
    game_iface.setup('classic')

    possible_moves = engine.moves(0, 4)

    assert len(possible_moves) == len(possible_moves2)
    for pos in possible_moves:
        assert pos in possible_moves2


possible_moves3 = [(8, 9), (9, 9), (9, 8), (9, 7),
                   (8, 7), (7, 7), (7, 8), (7, 9)]


def test_moves3():
    engine = Engine()
    game_iface = GameInterface(engine)
    game_iface.setup('classic')

    possible_moves = engine.moves(8, 8)

    assert len(possible_moves) == len(possible_moves3)
    for pos in possible_moves:
        assert pos in possible_moves3
