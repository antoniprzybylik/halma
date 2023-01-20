# Silnik gry Halma. Zawiera klasę
# Engine odpowiedzialną za operacje
# na planszy i zarządzanie grą.
#
# Autor: Antoni Przybylik

from halma.defs import STATE
from halma.defs import PLAYER

from random import randint


class ModeError(Exception):
    """! Wyjątek rzucany gdy gra nie wspiera rządanego trybu. """

    def __init__(self, obj):
        super().__init__('Unknown or invalid mode.')


class Engine:
    """! Reprezentuje grę Halma. """

    def __init__(self):
        """! Konstruktor klasy game. """
        self._board = [[STATE.EMPTY]*16 for i in range(16)]

        self.supported_modes = ['classic', 'random']

        self.mode = None
        self.move = 1  # Obecny ruch.
        self.moving_player = PLAYER.WHITE  # Teraz ruszający się gracz.

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
                self._board[i][j] = STATE.BLACK

        # Ustawiamy obóz Białego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                self._board[15 - i][15 - j] = STATE.WHITE

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

                if (self._board[i][j] == STATE.EMPTY):
                    break

            self._board[i][j] = STATE.BLACK

        # Ustawiamy białe pionki.
        for k in range(0, 19):
            # Losujemy pozycję dopóki
            # nie trafimy na puste pole.
            while True:
                i = randint(0, 15)
                j = randint(0, 15)

                if (self._board[i][j] == STATE.EMPTY):
                    break

            self._board[i][j] = STATE.WHITE

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
                self._board[y+dy][x+dx] == STATE.EMPTY):    # noqa E129

                if (len(visited) == 0):
                    possible.append((y+dy, x+dx))

            elif (self._validate_pos(y+2*dy, x+2*dx, visited) and
                  self._board[y+2*dy][x+2*dx] == STATE.EMPTY):

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

        if (value not in STATE):
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

        if (value not in STATE):
            raise ValueError('Corrupted data.')

        return value

    def _state_to_str(self, value):
        """! Zamienia obiekt typu wyliczeniowego state na napis. """

        if (value == STATE.EMPTY):
            return 'EMPTY'
        if (value == STATE.WHITE):
            return 'WHITE'
        if (value == STATE.BLACK):
            return 'BLACK'

        raise ValueError('Unknown state.')

    def _str_to_state(self, string):
        """! Zamienia napis na obiekt typu wyliczeniowego state. """

        if (string == 'EMPTY'):
            return STATE.EMPTY
        if (string == 'WHITE'):
            return STATE.WHITE
        if (string == 'BLACK'):
            return STATE.BLACK

        raise ValueError('Unknown state.')

    def _player_to_str(self, value):
        """! Zamienia obiekt typu wyliczeniowego player na napis. """

        if (value == PLAYER.WHITE):
            return 'WHITE'
        if (value == PLAYER.BLACK):
            return 'BLACK'

        raise ValueError('Unknown state.')

    def _str_to_player(self, string):
        """! Zamienia napis na obiekt typu wyliczeniowego player. """

        if (string == 'WHITE'):
            return PLAYER.WHITE
        if (string == 'BLACK'):
            return PLAYER.BLACK

        raise ValueError('Unknown state.')

    def dump_state(self):
        """! Zapisuje swój stan do słownika.

        @return Słownik ze stanem klasy Engine.
        """

        str_board = [[self._state_to_str(self._board[i][j])
                      for j in range(16)]
                     for i in range(16)]

        engine_state = {
                'mode': self.mode,
                'move': self.move,
                'moving_player': self._player_to_str(self.moving_player),
                'board': str_board,
        }

        return engine_state

    def load_state(self, engine_state):
        """! Wczytuje grę ze słownika.

        @param engine_state Słownik ze stanem silnika.
        """

        self.mode = engine_state.get('mode', None)
        if (self.mode is None):
            raise ValueError('Corrupted file.')

        move_str = engine_state.get('move', None)
        if (move_str is None):
            raise ValueError('Corrupted file.')

        self.move = int(move_str)

        moving_player_str = engine_state.get('moving_player', None)
        if (moving_player_str is None):
            raise ValueError('Corrupted file.')

        self.moving_player = self._str_to_player(moving_player_str)

        str_board = engine_state.get('board', None)
        if (str_board is None):
            raise ValueError('Corrupted file.')

        self._board = [[self._str_to_state(str_board[i][j])
                        for j in range(16)]
                       for i in range(16)]
