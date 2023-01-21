# Implementuje bazową klasę bota
# dziedziczącą po zwykłym graczu.
#
# Autor: Antoni Przybylik

from halma.defs import STATE
from halma.defs import PLAYER
from halma.defs import CAMP

from halma.player import Player


class GameBot(Player):
    """! Bazowa klasa bota. """

    def __init__(self, plr, engine):
        """! Konstruktor klasy GameBot.

        @param plr Gracz (biały/czarny).
        @param engine Referencja na obiekt Engine.
        """
        super().__init__(plr, engine)

    def _apply_move(self, field1, field2):
        """! Wykonuje ruch.

        @param field1 Pole z którego chcemy się ruszyć.
        @param field2 Pole na które chcemy się ruszyć.
        """

        on_field1 = self._engine.read_field(*field1)
        self._engine.set_field(*field1, STATE.EMPTY)
        self._engine.set_field(*field2, on_field1)

        if (self._engine.moving_player == PLAYER.WHITE):
            # Jeżeli teraz ruszał się biały, to
            # teraz jest kolej na czarnego.
            self._engine.moving_player = PLAYER.BLACK
        else:
            # Jeżeli w danym ruchu ruszył się czarny,
            # przechodzimy do następnego ruchu.
            self._engine.moving_player = PLAYER.WHITE
            self._engine.move += 1

    def _in_camp(self, y, x):
        """! Sprawdza w jakim obozie znajduje się pole.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.

        @return W jakim obozie znajduje się pole.
        """

        # Sprawdzamy, czy jest w obozie Czarnego.
        if (x in range(0, 5) and
                y in range(0, [5, 5, 4, 3, 2][x])):
            return CAMP.BLACK

        # Sprawdzamy, czy jest w obozie Białego.
        if (x in range(11, 16) and
                15-y in range(0, [5, 5, 4, 3, 2][15-x])):
            return CAMP.WHITE

        return None

    def make_move(self):
        """! Wykonuje ruch.

        @return Wykonany ruch.
        """
        pass
