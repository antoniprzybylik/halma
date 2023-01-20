# Implementuje bazową klasę bota
# dziedziczącą po zwykłym graczu.
#
# Autor: Antoni Przybylik

from halma.defs import STATE
from halma.defs import PLAYER

from halma.player import Player


class GameBot(Player):
    """! Bazowa klasa bota. """

    def __init__(self, plr, game):
        """! Konstruktor klasy GameBot.

        @param plr Gracz (biały/czarny).
        @param game Referencja na obiekt Game.
        """
        super().__init__(plr, game)

    def _apply_move(self, field1, field2):
        """! Wykonuje ruch.

        @param field1 Pole z którego chcemy się ruszyć.
        @param field2 Pole na które chcemy się ruszyć.
        """

        on_field1 = self._game.read_field(*field1)
        self._game.set_field(*field1, STATE.EMPTY)
        self._game.set_field(*field2, on_field1)

        if (self._game.moving_player == PLAYER.WHITE):
            # Jeżeli teraz ruszał się biały, to
            # teraz jest kolej na czarnego.
            self._game.moving_player = PLAYER.BLACK
        else:
            # Jeżeli w danym ruchu ruszył się czarny,
            # przechodzimy do następnego ruchu.
            self._game.moving_player = PLAYER.WHITE
            self._game.move += 1

    def make_move(self):
        """! Wykonuje ruch. """
        pass
