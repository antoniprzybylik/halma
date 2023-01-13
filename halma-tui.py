#!/usr/bin/python3

import halma
from halma import state

# Używam biblioteki curses
# do implementacji TUI.
#
# Moduł sys używam tylko
# do wyjścia programu
# w przypadku błędu.
import curses
from curses.textpad import Textbox
import sys


class TerminalNotSupportedError(Exception):
    """! Wyjątek rzucany gdy terminal nie ma wymaganych funkcji. """

    def __init__(self):
        super().__init__('Terminal not supported.')


class WindowTooSmallError(Exception):
    """! Wyjątek rzucany gdy okno terminala jest za małe. """
    def __init__(self):
        super().__init__('Window is too small.')


class HalmaTui:
    """! Reprezentuje interfejs graficzny. """

    def __init__(self):
        self._stdscr = None
        self._game = halma.Game()

    def _check_scr(self):
        """! Sprawdza, czy można uruchomić grę w trybie TUI.

        Żeby gra działała w terminalu musi on mieć kolory i
        pozwalać na ich zmianę, rozmiar okna terminala musi
        wynosić co najmniej 70x35.
        """

        if (not curses.has_colors() or not curses.can_change_color()):
            raise TerminalNotSupportedError()

        y, x = self._stdscr.getmaxyx()
        if (x < 70 or y < 35):
            raise WindowTooSmallError()

    def _curses_color(self, packed):
        """! Zapisuje kolor w konwencji Curses.

        Zamienia standardowy zapis koloru RGB
        w postaci 6-cyfrowej liczby w systemie szesnastkowym
        na kolor według konwencji używanej w bibliotece
        Curses, gdzie wartości kolorów są od 1 do 1000.

        Przykład:
        curses_color(0x80ff00) = (501, 1000, 0) ~= (500, 1000, 0)

        @param packed Kolor w standardowym zapisie.

        @return Kolor w konwencji Curses.
        """

        r = int(((packed >> 16) & 0xff) * (1000/0xff))
        g = int(((packed >> 8) & 0xff) * (1000/0xff))
        b = int((packed & 0xff) * (1000/0xff))

        return (r, g, b)

    def _print_header(self, move, player):
        """! Rysuje nagłówek.

        @param move Numer ruchu.
        @param player Gracz którego jest ruch.
        """

        y, x = self._stdscr.getmaxyx()

        left_aligned_str = ' HALMA 1.0'
        right_aligned_str = f'move: {move} player: {player} '
        gap_str = ' ' * (x -
                         len(left_aligned_str) -
                         len(right_aligned_str))

        self._stdscr.addstr(left_aligned_str, self._header_attr)
        self._stdscr.addstr(gap_str, self._header_attr)
        self._stdscr.addstr(right_aligned_str, self._header_attr)

    def _print_help(self):
        """! Rysuje pasek z pomocą. """
        help_msg = 'q - quit  m - move'

        self._stdscr.addstr('  ' + help_msg)
        self._stdscr.addstr('\n')

    def _field_label(self, num):
        """! Zamienia numer pola na podpis przy nim.

        @param num Numer pola.

        @return Podpis przy polu.
        """
        return chr(ord('A')+num)

    def _print_label_row(self, left_gap_str):
        """! Rysuje wiersz z podpisami pól.

        @param left_gap_str Przestrzeń po lewej stronie szachownicy.
        """

        self._stdscr.addstr(left_gap_str)

        # Górny wiersz z podpisami nie jest podpisany
        # z lewej. Zamiast podpisu rysujemy dwie spacje.
        self._stdscr.addstr('  ')

        for i in range(0, 16*4):
            ri = i // 4
            if ((i % 4) == 1):
                self._stdscr.addstr(self._field_label(ri))
            else:
                self._stdscr.addstr(' ')

        self._stdscr.addstr('\n')

    def _dialog(self, text, size_y, size_x):
        """! Wyświetla okno dialogowe na środku ekranu.

        @param text Tekst w oknie.
        @param size_y Wysokość.
        @param size_x Szerokość.

        @return Tekst wprowadzony przez użytkownika.
        """

        screen_y, screen_x = self._stdscr.getmaxyx()

        if (size_y < 7 or size_x < 8):
            raise ValueError("Too small requested size of dialog box.")

        if (size_y > screen_y or size_x > screen_x):
            raise ValueError("Too large requested size of dialog box.")

        # Pozycja dialog boxa.
        pos_x = (screen_x - size_x) // 2
        pos_y = (screen_y - size_y) // 2

        dialog_box = curses.newwin(size_y, size_x, pos_y, pos_x)
        dialog_box.bkgd(' ', self._dialogbox_attrs['DIALOG'])
        dialog_box.addstr(1, 1, text)

        # Pozycja pola wejściowego w dialog box'ie.
        input_window_pos = 3 + (size_y - 4 - 3) // 2

        input_window = dialog_box.subwin(3, size_x - 2,
                                         pos_y + input_window_pos,
                                         pos_x + 1)
        input_window.border()

        input_field_window = input_window.subwin(1, size_x - 4,
                                                 pos_y + input_window_pos + 1,
                                                 pos_x + 2)
        input_field_window.bkgd(' ', self._dialogbox_attrs['INPUT'])
        input_field = Textbox(input_field_window)

        dialog_box.refresh()

        curses.curs_set(1)
        input_field.edit()
        curses.curs_set(0)

        return input_field.gather()

    def _draw_main_window(self):
        """! Draws main UI window. """
        board = self._game.get_board()

        # Na górze rysujemy nagłówek.
        self._print_header(1, 'white')

        # Pod nagłówkiem rysujemy pasek pomocy.
        self._print_help()

        screen_y, screen_x = self._stdscr.getmaxyx()

        # Pusta przestrzeń po lewej stronie szachownicy i
        # na górze szachownicy.
        #
        # Przestrzeń z lewej: szerokość ekranu - 2*szerokość
        #                     podpisu pod polem
        #
        # Przestrzeń z prawej: wysokość ekranu - 2*szerokość
        #                      podpisu pod polem - szerokość
        #                      nagłówka i paska pomocy
        left_gap_str = ' ' * ((screen_x - 4*16 - 4) // 2)
        upper_gap_str = '\n' * ((screen_y - 2*16 - 4 - 2) // 2)

        self._stdscr.addstr(upper_gap_str)

        # Nad szachownicą rysujemy wiersz z podpisami pól.
        self._print_label_row(left_gap_str)

        # Rysujemy pola rozmiaru 4x2.
        #
        # ri, rj oznaczają współrzędne
        # pola terminala licząc od początku
        # szachownicy.
        #
        # i, j oznaczają współrzędne
        # obecnej kratki szachownicy.
        for ri in range(0, 16*2):
            i = ri // 2

            # Pusta przestrzeń po lewej stronie szachownicy.
            # Rysujemy ją przed każdym wierszem szachownicy.
            self._stdscr.addstr(left_gap_str)

            # Podpis i-tego wierza planszy z lewej strony.
            if ((ri % 2) == 0):
                self._stdscr.addstr(self._field_label(i) + ' ')
            else:
                self._stdscr.addstr('  ')

            for rj in range(0, 16*4):
                j = rj // 4

                field_char = ' '
                attr = None

                if (board[i][j] == state.WHITE and
                        (i+j) % 2 == 0):
                    attr = self._gameboard_attrs['WW']
                    field_char = 'w'

                if (board[i][j] == state.WHITE and
                        (i+j) % 2 == 1):
                    attr = self._gameboard_attrs['WB']
                    field_char = 'w'

                if (board[i][j] == state.BLACK and
                        (i+j) % 2 == 0):
                    attr = self._gameboard_attrs['BW']
                    field_char = 'm'

                if (board[i][j] == state.BLACK and
                        (i+j) % 2 == 1):
                    attr = self._gameboard_attrs['BB']
                    field_char = 'm'

                if (board[i][j] == state.EMPTY and
                        (i+j) % 2 == 0):
                    attr = self._gameboard_attrs['WW']

                if (board[i][j] == state.EMPTY and
                        (i+j) % 2 == 1):
                    attr = self._gameboard_attrs['BB']

                if (attr is None):
                    raise ValueError('Unknown field state.')

                if (rj % 4 == 1 and not ri % 2):
                    to_print = field_char
                else:
                    to_print = ' '

                self._stdscr.addstr(to_print, attr)

            # Podpis i-tego wierza planszy z prawej strony.
            if ((ri % 2) == 0):
                self._stdscr.addstr(' ' + self._field_label(i))

            self._stdscr.addstr('\n')

        # Pod szachownicą rysujemy wiersz z podpisami pól.
        self._print_label_row(left_gap_str)

    def _mainloop(self):
        """! Główna pętla gry. """

        while True:
            self._stdscr.clear()
            self._draw_main_window()
            self._stdscr.refresh()

            key = self._stdscr.getkey()

            if (key == 'q'):
                msg = self._dialog('Do you really want to quit? '
                                   'Type \"YES\" to confirm.', 7, 54)
                msg = msg.rstrip()

                if (msg == 'YES'):
                    break

            if (key == 'm'):
                msg = self._dialog('Enter your move:', 7, 30)

    def _setup_colors(self):
        """! Inicjalizuje kolory, które będą używane w UI. """

        # Kolory planszy.
        # Zaczynają się od 230.
        COLOR_BLACK_FIELD = 230
        COLOR_WHITE_FIELD = 231
        COLOR_WHITE_STONE = 232
        COLOR_BLACK_STONE = 233

        curses.init_color(COLOR_BLACK_FIELD, *self._curses_color(0x444444))
        curses.init_color(COLOR_WHITE_FIELD, *self._curses_color(0xa8a8a8))
        curses.init_color(COLOR_WHITE_STONE, *self._curses_color(0xffffff))
        curses.init_color(COLOR_BLACK_STONE, *self._curses_color(0x000000))

        # Pary kolorów planszy.
        curses.init_pair(1, COLOR_WHITE_STONE, COLOR_WHITE_FIELD)
        curses.init_pair(2, COLOR_BLACK_STONE, COLOR_WHITE_FIELD)
        curses.init_pair(3, COLOR_WHITE_STONE, COLOR_BLACK_FIELD)
        curses.init_pair(4, COLOR_BLACK_STONE, COLOR_BLACK_FIELD)

        self._gameboard_attrs = {
                'WW': curses.color_pair(1),
                'BW': curses.color_pair(2),
                'WB': curses.color_pair(3),
                'BB': curses.color_pair(4),
        }

        # Kolory nagłówka.
        # Zaczynają się od 240
        COLOR_HEADER_BG = 240
        COLOR_HEADER_FG = 241
        curses.init_color(COLOR_HEADER_BG, *self._curses_color(0xeeeeee))
        curses.init_color(COLOR_HEADER_FG, *self._curses_color(0x502040))

        # Para kolorów nagłówka.
        curses.init_pair(11, COLOR_HEADER_FG, COLOR_HEADER_BG)
        self._header_attr = curses.color_pair(11)

        # Kolory dialog boxa.
        # Zaczynają się od 250
        COLOR_DIALOG_BG = 250
        COLOR_DIALOG_FG = 251
        COLOR_INPUT_BG = 252
        COLOR_INPUT_FG = 253
        curses.init_color(COLOR_DIALOG_BG, *self._curses_color(0x666666))
        curses.init_color(COLOR_DIALOG_FG, *self._curses_color(0x000000))
        curses.init_color(COLOR_INPUT_BG, *self._curses_color(0x0000a0))
        curses.init_color(COLOR_INPUT_FG, *self._curses_color(0xeeee00))

        # Pary kolorów dialog boxa.
        curses.init_pair(21, COLOR_DIALOG_FG, COLOR_DIALOG_BG)
        curses.init_pair(22, COLOR_INPUT_FG, COLOR_INPUT_BG)

        self._dialogbox_attrs = {
                'DIALOG': curses.color_pair(21),
                'INPUT': curses.color_pair(22),
        }

    def _setup(self):
        """! Funkcja ustawiająca grę. """
        # FIXME: Trzeba dać do wyboru.
        self._game.setup('classic')

        # Sprawdzam, czy w danym terminalu
        # można uruchomić grę.
        self._check_scr()

        curses.start_color()
        curses.use_default_colors()

        # Zapisujemy kolory.
        self._saved_colors = [curses.color_content(i)
                              for i in range(curses.COLORS)]

        self._setup_colors()

        # Wyłącz pokazywanie kursora.
        curses.curs_set(0)

    def _exit(self):
        """! Funkcja na wyjście z gry. """
        # Przywracamy zapisane kolory.
        for i in range(curses.COLORS):
            curses.init_color(i, *self._saved_colors[i])

    def _exec(self, stdscr):
        """! Funkcja pomocnicza dla exec. """
        self._stdscr = stdscr

        self._setup()
        self._mainloop()
        self._exit()

    def exec(self):
        """! Wyświetla TUI. """
        curses.wrapper(self._exec)


if __name__ == "__main__":
    tui = HalmaTui()

    try:
        tui.exec()
    except TerminalNotSupportedError:
        sys.exit('Your terminal is not supported... :(')
    except WindowTooSmallError:
        sys.exit('Your terminal window is too small... :(')
