# Tekstowy interfejs użytkownika (TUI)
# do gry Halma.
#
# Autor: Antoni Przybylik

from halma.defs import PLAYER

from halma.engine import Engine
from halma.iface import GameInterface
from halma.game import Game

from bots.generic import GameBot
from bots.random_bot import RandomBot
from bots.forward_bot import ForwardBot
from bots.minimax_bot import MinimaxBot
from bots.agressive_minimax_bot import AgressiveMinimaxBot

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
        self._moves_bar = ' '*40

    def _mainloop(self):
        """! Główna pętla gry. """

        while True:
            self._tui.draw_main_window(self._game_iface.get_board(),
                                       self._game_iface.current_move(),
                                       self._game_iface.moving_player(),
                                       self._moves_bar,
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
                    player = self._game.get_player(PLAYER.WHITE)
                else:
                    player = self._game.get_player(PLAYER.BLACK)

                thinking_box = None
                # Jeżeli gracz jest botem należy
                # wyświetlić okienko "Myślę...".
                if (isinstance(player, GameBot)):
                    thinking_box = self._tui.get_message_box("Thinking...",
                                                             3, 15)

                move = player.make_move()
                if (move is not None):
                    # Aktualizujemy pasek ruchów.
                    self._moves_bar += str(move)
                    self._moves_bar = self._moves_bar[-40:]

                if (thinking_box is not None):
                    del thinking_box

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
                                      ' 3. Minimax bot.\n'
                                      ' 4. Agressive Minimax bot.\n'
                                      ' 5. Human.', 15, 54)

        while True:
            if (choice_str is not None):
                choice_str = choice_str.rstrip()
                if (len(choice_str) == 1 and
                        ord(choice_str) in range(ord('1'), ord('6'))):
                    break

            choice_str = self._tui.dialog('Invalid!\n'
                                          ' Select white player:\n'
                                          ' 1. Random bot.\n'
                                          ' 2. Forward bot.\n'
                                          ' 3. Minimax bot.\n'
                                          ' 4. Agressive Minimax bot.\n'
                                          ' 5. Human.', 17, 54)

        if (choice_str == '1'):
            self._game.set_player(PLAYER.WHITE,
                                  RandomBot(PLAYER.WHITE,
                                            self._engine))
        elif (choice_str == '2'):
            self._game.set_player(PLAYER.WHITE,
                                  ForwardBot(PLAYER.WHITE,
                                             self._engine))
        elif (choice_str == '3'):
            self._game.set_player(PLAYER.WHITE,
                                  MinimaxBot(PLAYER.WHITE,
                                             self._engine))
        elif (choice_str == '4'):
            self._game.set_player(PLAYER.WHITE,
                                  AgressiveMinimaxBot(PLAYER.WHITE,
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
                                      ' 3. Minimax bot.\n'
                                      ' 4. Agressive Minimax bot.\n'
                                      ' 5. Human.', 15, 54)

        while True:
            if (choice_str is not None):
                choice_str = choice_str.rstrip()
                if (len(choice_str) == 1 and
                        ord(choice_str) in range(ord('1'), ord('6'))):
                    break

            choice_str = self._tui.dialog('Invalid!\n'
                                          ' Select black player:\n'
                                          ' 1. Random bot.\n'
                                          ' 2. Forward bot.\n'
                                          ' 3. Minimax bot.\n'
                                          ' 4. Agressive Minimax bot.\n'
                                          ' 5. Human.', 17, 54)

        if (choice_str == '1'):
            self._game.set_player(PLAYER.BLACK,
                                  RandomBot(PLAYER.BLACK,
                                            self._engine))
        elif (choice_str == '2'):
            self._game.set_player(PLAYER.BLACK,
                                  ForwardBot(PLAYER.BLACK,
                                             self._engine))
        elif (choice_str == '3'):
            self._game.set_player(PLAYER.BLACK,
                                  MinimaxBot(PLAYER.BLACK,
                                             self._engine))
        elif (choice_str == '4'):
            self._game.set_player(PLAYER.BLACK,
                                  AgressiveMinimaxBot(PLAYER.BLACK,
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
