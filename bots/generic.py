# Implementuje bazową klasę bota.
#
# Autor: Antoni Przybylik

from halma.game import state
from halma.game import player


class GameBot:
    """! Bazowa klasa bota. """

    def __init__(self, game):
        """! Konstruktor klasy GameBot.

        @param game Obiekt klasy Game.
        """
        self._game = game

    def _apply_move(self, field1, field2):
        """! Wykonuje ruch.

        @param field1 Pole z którego chcemy się ruszyć.
        @param field2 Pole na które chcemy się ruszyć.
        """

        on_field1 = self._game.read_field(*field1)
        self._game.set_field(*field1, state.EMPTY)
        self._game.set_field(*field2, on_field1)

        if (self._game.moving_player == player.WHITE):
            # Jeżeli teraz ruszał się biały, to
            # teraz jest kolej na czarnego.
            self._game.moving_player = player.BLACK
        else:
            # Jeżeli w danym ruchu ruszył się czarny,
            # przechodzimy do następnego ruchu.
            self._game.moving_player = player.WHITE
            self._game.move += 1

    def make_move(self):
        """! Wykonuje ruch. """
        pass
