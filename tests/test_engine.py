# Testy jednostkowe dla metod klasy Engine,
# która jest w pliku halma/engine.py.
#
# Autor: Antoni Przybylik

from halma.engine import Engine
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
