# Testy jednostkowe dla metod klasy Engine,
# która jest w pliku halma/engine.py.
#
# Autor: Antoni Przybylik

from halma.engine import Engine
from halma.iface import GameInterface

from halma.defs import STATE


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


state1 = {"mode": "classic", "move": 19, "moving_player": "BLACK", "board": [["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "BLACK", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "EMPTY", "EMPTY", "BLACK", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "EMPTY", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "EMPTY", "BLACK", "BLACK", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "BLACK", "BLACK", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "BLACK", "BLACK", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "WHITE", "EMPTY", "EMPTY", "EMPTY"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE", "WHITE", "WHITE", "WHITE", "WHITE"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "EMPTY", "WHITE", "EMPTY", "WHITE", "WHITE", "WHITE"], ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "WHITE", "EMPTY", "WHITE", "WHITE"]]}  # noqa: E501


def test_dump_load():
    engine = Engine()
    engine.load_state(state1)

    state2 = engine.dump_state()
    assert str(state1) == str(state2)


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

    for pos in possible_moves:
        assert pos in possible_moves1
