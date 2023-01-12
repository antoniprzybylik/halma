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
import sys


class TerminalNotSupportedError(Exception):
    """! Wyjątek rzucany gdy terminal nie ma wymaganych funkcji. """

    def __init__(self):
        super().__init__('Terminal not supported.')


class WindowTooSmallError(Exception):
    """! Wyjątek rzucany gdy okno terminala jest za małe. """
    def __init__(self):
        super().__init__('Window is too small.')


def check_scr(stdscr):
    """! Sprawdza, czy można uruchomić grę w trybie TUI.

    Żeby gra działała w terminalu musi on mieć kolory i
    pozwalać na ich zmianę, rozmiar okna terminala musi
    wynosić co najmniej 70x35.

    @param stdscr Ekran Curses.
    """

    if (not curses.has_colors() or not curses.can_change_color()):
        raise TerminalNotSupportedError()

    y, x = stdscr.getmaxyx()
    if (x < 70 or y < 35):
        raise WindowTooSmallError()


def curses_color(packed):
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


def print_header(stdscr, attr, move, player):
    """! Rysuje nagłówek.

    @param stdscr Ekran Curses.
    @param attr Własności czcionki.
    @param move Numer ruchu.
    @param player Gracz którego jest ruch.
    """

    y, x = stdscr.getmaxyx()

    left_aligned_str = ' HALMA 1.0'
    right_aligned_str = f'move: {move} player: {player} '
    gap_str = ' ' * (x -
                     len(left_aligned_str) -
                     len(right_aligned_str))

    stdscr.addstr(left_aligned_str, attr)
    stdscr.addstr(gap_str, attr)
    stdscr.addstr(right_aligned_str, attr)
    stdscr.addstr('\n')


def field_label(num):
    """! Zamienia numer pola na podpis przy nim.

    @param num Numer pola.

    @return Podpis przy polu.
    """
    return chr(ord('A')+num)


def print_label_row(stdscr, left_gap_str):
    """! Rysuje wiersz z podpisami pól.

    @param stdscr Ekran Curses.
    @param left_gap_str Przestrzeń po lewej stronie szachownicy.
    """

    stdscr.addstr(left_gap_str)

    # Górny wiersz z podpisami nie jest podpisany
    # z lewej. Zamiast podpisu rysujemy dwie spacje.
    stdscr.addstr('  ')

    for i in range(0, 16*4):
        ri = i // 4
        if ((i % 4) == 1):
            stdscr.addstr(field_label(ri))
        else:
            stdscr.addstr(' ')

    stdscr.addstr('\n')


def main(stdscr):
    """! Główna funkcja gry.

    Główna funkcja gry.
    W przyszłości dam rysowanie
    do osobnej funkcji, a tutaj
    ogólne rzeczy.

    @param stdscr Ekran Curses.
    """

    game = halma.game()
    game.setup('classic')

    board = game.get_board()

    # Sprawdzam, czy w danym terminalu
    # można uruchomić grę.
    check_scr(stdscr)

    curses.start_color()
    curses.use_default_colors()

    # Zapisujemy kolory.
    saved_colors = [curses.color_content(i)
                    for i in range(curses.COLORS)]

    # Kolory planszy.
    # Zaczynają się od 240.
    COLOR_BLACK_FIELD = 240
    COLOR_WHITE_FIELD = 241
    COLOR_WHITE_STONE = 242
    COLOR_BLACK_STONE = 243

    curses.init_color(COLOR_BLACK_FIELD, *curses_color(0x444444))
    curses.init_color(COLOR_WHITE_FIELD, *curses_color(0xa8a8a8))
    curses.init_color(COLOR_WHITE_STONE, *curses_color(0xffffff))
    curses.init_color(COLOR_BLACK_STONE, *curses_color(0x000000))

    # Pary kolorów planszy.
    curses.init_pair(1, COLOR_WHITE_STONE, COLOR_WHITE_FIELD)
    curses.init_pair(2, COLOR_BLACK_STONE, COLOR_WHITE_FIELD)
    curses.init_pair(3, COLOR_WHITE_STONE, COLOR_BLACK_FIELD)
    curses.init_pair(4, COLOR_BLACK_STONE, COLOR_BLACK_FIELD)

    # Kolory nagłówka.
    # Zaczynają się od 250
    COLOR_HEADER_BG = 250
    COLOR_HEADER_FG = 251
    curses.init_color(COLOR_HEADER_BG, *curses_color(0xeeeeee))
    curses.init_color(COLOR_HEADER_FG, *curses_color(0x502040))

    # Para kolorów nagłówka.
    curses.init_pair(11, COLOR_HEADER_FG, COLOR_HEADER_BG)
    header_attr = curses.color_pair(11)

    curses.curs_set(0)
    stdscr.clear()

    # Na górze rysujemy nagłówek.
    print_header(stdscr, header_attr, 1, 'white')

    screen_y, screen_x = stdscr.getmaxyx()

    # Pusta przestrzeń po lewej stronie szachownicy i
    # na górze szachownicy.
    left_gap_str = ' ' * ((screen_x - 4*16 - 4) // 2)
    upper_gap_str = '\n' * ((screen_y - 2*16 - 2 - 1 - 2) // 2)

    stdscr.addstr(upper_gap_str)

    # Nad szachownicą rysujemy wiersz z podpisami pól.
    print_label_row(stdscr, left_gap_str)

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
        stdscr.addstr(left_gap_str)

        # Podpis i-tego wierza planszy z lewej strony.
        if ((ri % 2) == 0):
            stdscr.addstr(field_label(i) + ' ')
        else:
            stdscr.addstr('  ')

        for rj in range(0, 16*4):
            j = rj // 4

            # Tło: 0 - białe, 2 - czarne.
            color_pair = 0 if ((i+j) % 2) else 2
            field_char = ' '

            if (board[i][j] == state.WHITE):
                color_pair += 1  # Biała czcionka.
                field_char = 'w'

            if (board[i][j] == state.BLACK):
                color_pair += 2  # Czarna czcionka.
                field_char = 'm'

            if (board[i][j] == state.EMPTY):
                color_pair += 1
                # Czcionka, której używamy na
                # pustym polu nie ma znaczenia

            attr = curses.color_pair(color_pair)

            if (rj % 4 == 1 and not ri % 2):
                to_print = field_char
            else:
                to_print = ' '

            stdscr.addstr(to_print, attr)

        # Podpis i-tego wierza planszy z prawej strony.
        if ((ri % 2) == 0):
            stdscr.addstr(' ' + field_label(i))

        stdscr.addstr('\n')

    # Pod szachownicą rysujemy wiersz z podpisami pól.
    print_label_row(stdscr, left_gap_str)

    stdscr.refresh()
    stdscr.getkey()

    # Przywracamy zapisane kolory.
    for i in range(curses.COLORS):
        curses.init_color(i, *saved_colors[i])


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except TerminalNotSupportedError:
        sys.exit('Your terminal is not supported... :(')
    except WindowTooSmallError:
        sys.exit('Your terminal window is too small... :(')
