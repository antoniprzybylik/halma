from enum import Enum


class ModeError(Exception):
    def __init__(self, obj):
        super().__init__('Unknown or invalid mode.')


class state(Enum):
    EMPTY = 1
    WHITE = 2
    BLACK = 3


class game:
    """
    supported_modes

    setup()
    moves()
    print()
    """
    def __init__(self):
        self._board = [[state.EMPTY]*16 for i in range(16)]
        self.supported_modes = ['classic']

        self.mode = None
        self.move = 1  # Obecny ruch.

    def setup(self, mode):
        """
        Setups the game.
        """

        if (type(mode) != str):
            raise ModeError(mode)
        if (mode not in self.supported_modes):
            raise ModeError(mode)

        self.mode = mode
        if (mode == 'classic'):
            self._classic_mode_setup()
            return

    def _classic_mode_setup(self):
        """
        Setups game in classic mode.
        This function is meant to be
        used throught setup method.
        """

        # Ustawiamy obóz Czarnego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                self._board[i][j] = state.BLACK

        # Ustawiamy obóz Białego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                self._board[15 - i][15 - j] = state.WHITE

    def moves(self, x, y):
        if (type(x) != int):
            raise TypeError('Invalid coordinates')
        if (type(x) != int):
            raise TypeError('Invalid coordinates')

        return self._moves(x, y)

    def _pos_on_board(self, x, y):
        if (x < 0 or y < 0):
            return False
        if (x > 15 or y > 15):
            return False
        return True

    def _pos_permitted(self, x, y, forbidden):
        if ((x, y) in forbidden):
            return False
        return True

    def _validate_pos(self, x, y, forbidden):
        if (self._pos_on_board(x, y) and
            self._pos_permitted(x, y, forbidden)):  # noqa: E129
            return True
        return False

    def _moves(self, x, y, visited=[]):
        delta_x = [-1, 0, 1, 1,  1,  0, -1, -1]
        delta_y = [ 1, 1, 1, 0, -1, -1, -1,  0]  # noqa: E201

        possible = []

        for dx, dy in zip(delta_x, delta_y):
            if (self._validate_pos(x+dx, y+dy, visited) and
                self._board[x+dx][y+dy] == state.EMPTY):    # noqa E129

                if (len(visited) == 0):
                    possible.append((x+dx, y+dy))

            elif (self._validate_pos(x+2*dx, y+2*dy, visited) and
                  self._board[x+2*dx][y+2*dy] == state.EMPTY):

                possible.append((x+2*dx, y+2*dy))

                # Unikamy kopiowania tablicy.
                # Dodajemy tylko do niej obecną
                # pozycję, a następnie ją usuwamy.
                visited.append((x, y))
                possible += self._moves(x+2*dx, y+2*dy, visited)
                visited.pop()

        return possible

    def get_board(self):
        """
        Returns gameboard.
        """

        return self._board

    def set_field(self, x, y, value):
        """
        Sets a field in some state.
        """

        if (not self._pos_on_board(x, y)):
            raise ValueError('No such a field.')

        if (value not in state):
            raise ValueError('Not a valid value for field.')

        self._board[x][y] = value

    def read_field(self, x, y):
        """
        Reads value from some field.
        """

        if (not self._pos_on_board(x, y)):
            raise ValueError('No such a field.')

        value = self._board[x][y]

        if (value not in state):
            raise ValueError('Corrupted data.')

        return value
