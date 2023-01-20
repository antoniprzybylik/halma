# Tekstowy interfejs użytkownika (TUI)
# do gry Halma.
#
# Autor: Antoni Przybylik

from halma.defs import PLAYER

from halma.engine import Engine
from halma.iface import GameInterface
from halma.game import Game

from bots.random_bot import RandomBot
from bots.forward_bot import ForwardBot

from ui.tui_generic import TuiEngine
from ui.tui_player import TuiPlayer

# Używam biblioteki curses
# do implementacji TUI.
import curses


class HalmaTui:
    """! Reprezentuje interfejs graficzny. """

    def __init__(self):
        """! Konstruktor klasy HalmaTui. """
        self._engine = Engine()
        self._game_iface = GameInterface(self._engine)

        self._game = Game(self._engine, self._game_iface)

        self._tui = None

    def _mainloop(self):
        """! Główna pętla gry. """

        while True:
            self._tui.draw_main_window(self._game_iface.get_board(),
                                       self._game_iface.current_move(),
                                       self._game_iface.moving_player(),
                                       self._game_iface.in_camp)

            key = self._tui.getkey()

            if (key == 'q'):
                msg = self._tui.dialog('Do you really want to quit? '
                                       'Type \"YES\" to confirm.', 7, 54)

                if (msg is not None):
                    msg = msg.rstrip()

                    if (msg == 'YES'):
                        # Kończymy pętlę główną gry.
                        break

            if (key == 'm'):
                if (self._game_iface.moving_player() == PLAYER.WHITE):
                    self._game.get_player(PLAYER.WHITE).make_move()
                else:
                    self._game.get_player(PLAYER.BLACK).make_move()

                # Sprawdzamy wygraną.
                winner = self._game_iface.get_winner()

                if (winner == PLAYER.WHITE):
                    self._tui.splash('White won!')

                    # Kończymy pętlę główną gry.
                    break

                if (winner == PLAYER.BLACK):
                    self._tui.splash('Black won!')

                    # Kończymy pętlę główną gry.
                    break

            if (key == 's'):
                filename = self._tui.dialog('Enter filename:', 7, 30)

                while True:
                    if (filename is None):
                        break

                    filename = filename.rstrip()

                    success = self._game.save(filename)
                    if (success):
                        break

                    filename = self._tui.dialog('Invalid!\n'
                                                ' Enter filename:', 9, 30)

    def _game_setup(self):
        """! Ustawia grę.

        Funkcja jest wywoływana na początku programu,
        daje możliwość wczytania gry z pliku lub
        utworzenia nowej i ustawienia jej ustawień.
        """
        choice_str = self._tui.dialog('1. New game.\n'
                                      ' 2. Load game.', 8, 54)

        while True:
            if (choice_str is not None):
                choice_str = choice_str.rstrip()
                if (len(choice_str) == 1 and
                        ord(choice_str) in range(ord('1'), ord('3'))):
                    break

            choice_str = self._tui.dialog('1. New game.\n'
                                          ' 2. Load game.', 8, 54)

        if (choice_str == '1'):
            self._new_game_setup()
        else:
            filename = self._tui.dialog('Enter filename:', 7, 30)

            while True:
                if (filename is not None):
                    filename = filename.rstrip()

                    try:
                        self._game.load(filename)
                    except (ValueError, EnvironmentError):
                        # Zostajemy w pętli.
                        pass
                    else:
                        break

                filename = self._tui.dialog('Invalid!\n'
                                            ' Enter filename:', 9, 30)

    def _new_game_setup(self):
        """! Funkcja ustawiająca nową grę.

        Ta funkcja jest wywoływana jeśli w _game_setup
        wybierzemy stworzenie nowej gry.
        """
        choice_str = self._tui.dialog('Select game setup:\n'
                                      ' 1. Classic.\n'
                                      ' 2. Random.', 9, 54)

        while True:
            if (choice_str is not None):
                choice_str = choice_str.rstrip()
                if (len(choice_str) == 1 and
                        ord(choice_str) in range(ord('1'), ord('3'))):
                    break

            choice_str = self._tui.dialog('Invalid!\n'
                                          ' Select game setup:\n'
                                          ' 1. Classic.\n'
                                          ' 2. Random.', 12, 54)

        if (choice_str == '1'):
            self._game_iface.setup('classic')
        else:
            self._game_iface.setup('random')

        choice_str = self._tui.dialog('Select white player:\n'
                                      ' 1. Random bot.\n'
                                      ' 2. Forward bot.\n'
                                      ' 3. Human.', 11, 54)

        while True:
            if (choice_str is not None):
                choice_str = choice_str.rstrip()
                if (len(choice_str) == 1 and
                        ord(choice_str) in range(ord('1'), ord('4'))):
                    break

                choice_str = self._tui.dialog('Invalid!\n'
                                              ' Select white player:\n'
                                              ' 1. Random bot.\n'
                                              ' 2. Forward bot.\n'
                                              ' 3. Human.', 13, 54)

        if (choice_str == '1'):
            self._game.set_player(PLAYER.WHITE,
                                  RandomBot(PLAYER.WHITE,
                                            self._engine))
        elif (choice_str == '2'):
            self._game.set_player(PLAYER.WHITE,
                                  ForwardBot(PLAYER.WHITE,
                                             self._engine))
        else:
            self._game.set_player(PLAYER.WHITE,
                                  TuiPlayer(PLAYER.WHITE,
                                            self._engine,
                                            self._game_iface,
                                            self._tui))

        choice_str = self._tui.dialog('Select black player:\n'
                                      ' 1. Random bot.\n'
                                      ' 2. Forward bot.\n'
                                      ' 3. Human.', 11, 54)

        while True:
            if (choice_str is not None):
                choice_str = choice_str.rstrip()
                if (len(choice_str) == 1 and
                        ord(choice_str) in range(ord('1'), ord('4'))):
                    break

            choice_str = self._tui.dialog('Invalid!\n'
                                          ' Select black player:\n'
                                          ' 1. Random bot.\n'
                                          ' 2. Forward bot.\n'
                                          ' 3. Human.', 13, 54)

        if (choice_str == '1'):
            self._game.set_player(PLAYER.BLACK,
                                  RandomBot(PLAYER.BLACK,
                                            self._engine))
        elif (choice_str == '2'):
            self._game.set_player(PLAYER.BLACK,
                                  ForwardBot(PLAYER.BLACK,
                                             self._engine))
        else:
            self._game.set_player(PLAYER.BLACK,
                                  TuiPlayer(PLAYER.BLACK,
                                            self._engine,
                                            self._game_iface,
                                            self._tui))

    def _exit(self):
        """! Funkcja na wyjście z gry. """
        del self._tui

    def _exec(self, stdscr):
        """! Funkcja pomocnicza dla exec.

        Ta funkcja jest punktem wejścia,
        który przekazujemy bibliotece curses.
        """
        self._tui = TuiEngine(stdscr)
        self._game.set_ui(self._tui)

        self._game_setup()
        self._mainloop()
        self._exit()

    def exec(self):
        """! Wyświetla TUI. """
        curses.wrapper(self._exec)
