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

        self._ui = None

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

    def set_ui(self, ui):
        """! Ustawia referencję na ui. """
        self._ui = ui

    def _player_type_str(self, player):
        """! Zamienia obiekt klasy dziedziczącej po Player na
        napis go identyfikujący. """
        if (isinstance(player, RandomBot)):
            return 'RANDOM_BOT'
        elif (isinstance(player, ForwardBot)):
            return 'FORWARD_BOT'
        else:
            return 'HUMAN'

    def _create_player_of_type(self, string, plr):
        """! Tworzy gracza danego typu. """
        if (string == 'RANDOM_BOT'):
            return RandomBot(plr, self._engine)
        elif (string == 'FORWARD_BOT'):
            return ForwardBot(plr, self._engine)
        else:
            return TuiPlayer(plr, self._engine, self._ui)

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
        # Nie zajmuję się tu obsługą błędów.
        # Wyjątek ma zostać obsłużony wyżej.
        with open(filename, 'r') as fp:
            game_data = json.load(fp)

        engine_state = game_data.get('engine', None)
        if (engine_state is None):
            raise ValueError('Corrupted file.')

        self._engine.load_state(engine_state)

        white_player_str = game_data.get('white_player', None)
        if (white_player_str is None):
            raise ValueError('Corrupted file.')

        self._white_player = self._create_player_of_type(
                                            white_player_str,
                                            PLAYER.WHITE)

        black_player_str = game_data.get('black_player', None)
        if (black_player_str is None):
            raise ValueError('Corrupted file.')

        self._black_player = self._create_player_of_type(
                                            black_player_str,
                                            PLAYER.BLACK)
