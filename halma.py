# Silnik gry Halma. Zawiera klasę
# Game odpowiedzialną za operacje
# na planszy i zarządzanie grą.
#
# Autor: Antoni Przybylik

from enum import Enum
from random import randint
import json


class ModeError(Exception):
    """! Wyjątek rzucany gdy gra nie wspiera rządanego trybu. """

    def __init__(self, obj):
        super().__init__('Unknown or invalid mode.')


class state(Enum):
    """! Stan pola planszy. """
    EMPTY = 1
    WHITE = 2
    BLACK = 3


class player(Enum):
    """! Gracz. """
    WHITE = 1
    BLACK = 2


class Game:
    """! Reprezentuje grę Halma.

    Parametry publiczne:
        supported_modes
        mode
        move
        moving_player

    Metody publiczne:
        setup()
        in_camp()
        moves()
        get_board()
        set_field()
        read_field()
        save()
        load()
    """

    def __init__(self):
        """! Konstruktor klasy game. """
        self._board = [[state.EMPTY]*16 for i in range(16)]

        self.supported_modes = ['classic', 'random']

        self.mode = None
        self.move = 1  # Obecny ruch.
        self.moving_player = player.WHITE  # Teraz ruszający się gracz.

    def setup(self, mode):
        """! Ustawia grę.

        Tą funkcję trzeba wykonać przed
        rozpoczęciem gry.

        @param mode Tryb gry.
        """

        if (type(mode) != str):
            raise ModeError(mode)
        if (mode not in self.supported_modes):
            raise ModeError(mode)

        self.mode = mode
        if (mode == 'classic'):
            self._classic_mode_setup()
            return
        if (mode == 'random'):
            self._random_mode_setup()
            return

    def _classic_mode_setup(self):
        """! Funkcja pomocnicza metody setup.

        Ustawia grę w trybie klasycznym.
        """

        # Ustawiamy obóz Czarnego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                self._board[i][j] = state.BLACK

        # Ustawiamy obóz Białego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                self._board[15 - i][15 - j] = state.WHITE

    def _random_mode_setup(self):
        """! Funkcja pomocnicza metody setup.

        Ustawia grę losowo.
        """

        # Ustawiamy czarne pionki.
        for k in range(0, 19):
            # Losujemy pozycję dopóki
            # nie trafimy na puste pole.
            while True:
                i = randint(0, 15)
                j = randint(0, 15)

                if (self._board[i][j] == state.EMPTY):
                    break

            self._board[i][j] = state.BLACK

        # Ustawiamy białe pionki.
        for k in range(0, 19):
            # Losujemy pozycję dopóki
            # nie trafimy na puste pole.
            while True:
                i = randint(0, 15)
                j = randint(0, 15)

                if (self._board[i][j] == state.EMPTY):
                    break

            self._board[i][j] = state.WHITE

    def moves(self, y, x):
        """! Znajduje wszystkie pola na które można wykonać ruch.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.

        @return Lista pól na które można wykonać ruch z danego pola.
        """
        if (type(y) != int):
            raise TypeError('Invalid coordinates')
        if (type(x) != int):
            raise TypeError('Invalid coordinates')

        return self._moves(y, x)

    def _pos_on_board(self, y, x):
        """! Sprawdza, czy pole jest na planszy.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.

        @return Czy pole jest na planszy.
        """
        if (y < 0 or x < 0):
            return False
        if (y > 15 or x > 15):
            return False
        return True

    def _pos_permitted(self, y, x, forbidden):
        """! Sprawdza, czy pole jest na liście pól zakazanych.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.
        @param forbidden Lista pól zakazanych.

        @return Czy pole jest na liście pól zakazanych.
        """
        if ((y, x) in forbidden):
            return False
        return True

    def _validate_pos(self, y, x, forbidden):
        """! Sprawdza, czy wolno się ruszyć na dane pole.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.
        @param visited Lista pól zakazanych.

        @return Czy wolno się ruszyć na dane pole.
        """
        if (self._pos_on_board(y, x) and
            self._pos_permitted(y, x, forbidden)):  # noqa: E129
            return True
        return False

    def _moves(self, y, x, visited=[]):
        """! Funkcja pomocnicza metody moves.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.
        @param visited Odwiedzone pola.

        @return Pola na które można się ruszyć.
        """
        delta_y = [-1, 0, 1, 1,  1,  0, -1, -1]
        delta_x = [ 1, 1, 1, 0, -1, -1, -1,  0]  # noqa: E201

        possible = []

        for dy, dx in zip(delta_y, delta_x):
            if (self._validate_pos(y+dy, x+dx, visited) and
                self._board[y+dy][x+dx] == state.EMPTY):    # noqa E129

                if (len(visited) == 0):
                    possible.append((y+dy, x+dx))

            elif (self._validate_pos(y+2*dy, x+2*dx, visited) and
                  self._board[y+2*dy][x+2*dx] == state.EMPTY):

                possible.append((y+2*dy, x+2*dx))

                # Unikamy kopiowania tablicy.
                # Dodajemy tylko do niej obecną
                # pozycję, a następnie ją usuwamy.
                visited.append((y, x))
                possible += self._moves(y+2*dy, x+2*dx, visited)
                visited.pop()

        return possible

    def get_board(self):
        """! Returns gameboard.

        @return Plansza.
        """

        return self._board

    def set_field(self, y, x, value):
        """! Ustawia pole w danym stanie.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.
        @param value Stan pola.
        """

        if (not self._pos_on_board(y, x)):
            raise ValueError('No such a field.')

        if (value not in state):
            raise ValueError('Not a valid value for field.')

        self._board[y][x] = value

    def read_field(self, y, x):
        """! Zwraca stan danego pola.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.

        @return Stan pola.
        """

        if (not self._pos_on_board(y, x)):
            raise ValueError('No such a field.')

        value = self._board[y][x]

        if (value not in state):
            raise ValueError('Corrupted data.')

        return value

    def _state_to_str(self, value):
        """! Zamienia obiekt typu wyliczeniowego state na napis. """

        if (value == state.EMPTY):
            return 'EMPTY'
        if (value == state.WHITE):
            return 'WHITE'
        if (value == state.BLACK):
            return 'BLACK'

        raise ValueError('Unknown state.')

    def _str_to_state(self, string):
        """! Zamienia napis na obiekt typu wyliczeniowego state. """

        if (string == 'EMPTY'):
            return state.EMPTY
        if (string == 'WHITE'):
            return state.WHITE
        if (string == 'BLACK'):
            return state.BLACK

        raise ValueError('Unknown state.')

    def _player_to_str(self, value):
        """! Zamienia obiekt typu wyliczeniowego player na napis. """

        if (value == player.WHITE):
            return 'WHITE'
        if (value == player.BLACK):
            return 'BLACK'

        raise ValueError('Unknown state.')

    def _str_to_player(self, string):
        """! Zamienia napis na obiekt typu wyliczeniowego player. """

        if (string == 'WHITE'):
            return player.WHITE
        if (string == 'BLACK'):
            return player.BLACK

        raise ValueError('Unknown state.')

    def save(self, filename):
        """! Zapisuje grę do pliku.

        @filename Nazwa pliku.

        @return Czy zapis się udał.
        """

        str_board = [[self._state_to_str(self._board[i][j])
                      for j in range(16)]
                     for i in range(16)]

        to_save = {
                'mode': self.mode,
                'move': self.move,
                'moving_player': self._player_to_str(self.moving_player),
                'board': str_board,
        }

        try:
            with open(filename, 'w') as fp:
                json.dump(to_save, fp)
        except EnvironmentError:
            # Zapis się nie udał bo
            # np. nie mamy uprawnień do pliku.
            return False

        return True

    def load(self, filename):
        """! Wczytuje grę z pliku.

        @filename Nazwa pliku.
        """

        game_data = None

        # Nie zajmuję się tu obsługą błędów.
        # Wyjątek ma zostać obsłużony wyżej.
        with open(filename, 'r') as fp:
            game_data = json.load(fp)

        self.mode = game_data.get('mode', None)
        if (self.mode is None):
            raise ValueError('Corrupted file.')

        self.move = game_data.get('move', None)
        if (self.move is None):
            raise ValueError('Corrupted file.')

        self.moving_player = game_data.get('moving_player', None)
        if (self.moving_player is None):
            raise ValueError('Corrupted file.')

        str_board = game_data.get('board', None)
        if (str_board is None):
            raise ValueError('Corrupted file.')

        self._board = [[self._str_to_state(str_board[i][j])
                        for j in range(16)]
                       for i in range(16)]
