# Klasa Game reprezentująca instancję
# całej gry. Zawiera obiekt Engine ze
# stanem silnika, a także obiekty klasy
# Player ze stanami graczy.
#
# Autor: Antoni Przybylik

from halma.defs import PLAYER

from bots.random_bot import RandomBot
from bots.forward_bot import ForwardBot

from ui.tui_player import TuiPlayer

import json


class Game:
    """! Klasa Game. """

    def __init__(self, engine, iface,
                 white_player=None,
                 black_player=None):
        """! Konstruktor klasy Game. """
        self._engine = engine
        self._game_iface = iface
        self._white_player = white_player
        self._black_player = black_player

    def get_player(self, which_plr):
        """! Zwracza gracza o danym kolorze.

        @plr Gracz (biały/czarny).

        @return Obiekt klasy Player.
        """

        if (which_plr == PLAYER.WHITE):
            return self._white_player
        else:
            return self._black_player

    def set_player(self, which_plr, player):
        """! Ustawia gracza o danym kolorze.

        @plr Gracz (biały/czarny).
        @player Obiekt klasy Player.
        """

        if (which_plr == PLAYER.WHITE):
            self._white_player = player
        else:
            self._black_player = player

    def _player_type_str(self, player):
        """! Zamienia obiekt klasy dziedziczącej po Player na
        napis go identyfikujący. """
        if (isinstance(player, RandomBot)):
            return 'RANDOM_BOT'
        elif (isinstance(player, ForwardBot)):
            return 'FORWARD_BOT'
        else:
            return 'HUMAN'

    def _create_player_of_type(self, string, plr, game, iface, ui):
        """! Tworzy gracza danego typu. """
        if (string == 'RANDOM_BOT'):
            return RandomBot(plr, game)
        elif (string == 'FORWARD_BOT'):
            return ForwardBot(plr, game)
        else:
            return TuiPlayer(plr, game, ui)

    def save(self, filename):
        to_save = {
                'engine': self._engine.dump_state(),
                'white_player': self._player_type_str(
                                        self._white_player),
                'black_player': self._player_type_str(
                                        self._black_player),
        }

        try:
            with open(filename, 'w') as fp:
                json.dump(to_save, fp)
        except EnvironmentError:
            # Zapis się nie udał bo
            # np. nie mamy uprawnień do pliku.
            return False

    def load(self, filename):
        # TODO
        pass
