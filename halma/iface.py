# Zawiera klasę GameInterface, której
# rolą jest stworzenie warstwy abstrakcji
# pomiędzy silnikiem (w klasie Engine), a
# użytkownikiem (tzn. modułem korzystającym
# z tej klasy).
#
# Klasa Engine wykonuje operacje ściśle związane
# z grą. Klasa GameInterface obsługuje np.
# ruch gracza przy pomocy wielu wywołań metod
# klasy Engine.
#
# Autor: Antoni Przybylik

from halma.defs import STATE
from halma.defs import PLAYER
from halma.defs import CAMP


class GameInterface:
    """! Reprezentuje interfejs gry. """

    def __init__(self, engine):
        """! Konstruktor klasy GameInterface.

        @param engine Obiekt klasy Engine.
        """
        self._engine = engine

    def get_board(self):
        """! Zwraca planszę do gry.

        @return Plansza do gry.
        """
        return self._engine.get_board()

    def setup(self, mode):
        """! Ustawia grę w żądanym stanie. """
        self._engine.setup(mode)

    def current_move(self):
        """! Zwraca numer obecnego ruchu.

        @return Numer ruchu.
        """
        return self._engine.move

    def moving_player(self):
        """! Gracz którego jest ruch w typie wyliczeniowym PLAYER.

        @return Gracz, którego jest ruch.
        """
        return self._engine.moving_player

    def _is_field_label(self, char):
        """! Sprawdza, czy znak jest ważnym podpisem pola.

        Żeby znak mógł być podpisem pola musi się
        zawierać w przedziale 'a'-'p' lub 'A'-'P'.
        Ta funkcja sprawdza, czy znajduje się w którymś
        z tych przedziałów.

        @param char Literka.

        @return Czy literka jest ważnym podpisem pola.
        """

        # Jeśli na wejściu nie mamy literki.
        if (len(char) != 1):
            return False

        if ((ord(char) > ord('p') or
             ord(char) < ord('a')) and
            (ord(char) > ord('P') or
             ord(char) < ord('A'))):
            return False

        return True

    def _validate_move_str(self, move_str):
        """! Sprawdza poprawność zapisu ruchu.

        Ruch ma być w formacie: XY-XY.

        @param move_str Zapis ruchu.

        @return Czy zapis jest poprawny.
        """

        if (len(move_str) != 5):
            return False

        if (self._is_field_label(move_str[0]) and
                self._is_field_label(move_str[1]) and
                move_str[2] == '-' and
                self._is_field_label(move_str[3]) and
                self._is_field_label(move_str[4])):
            return True

        return False

    def _validate_move(self, field1, field2):
        """! Sprawdza, czy obecnie ruszający się gracz może wykonać taki ruch.

        @param field1 Pole z którego chcemy się ruszyć.
        @param field2 Pole na które chcemy się ruszyć.

        @return Czy można wykonać ruch.
        """

        # Najpierw należy sprawdzić, czy na polu
        # z którego chcemy się ruszyć stoi kamień
        # gracza, który ma teraz swój ruch.
        if (self._engine.moving_player == PLAYER.WHITE):
            field_state = STATE.WHITE
        else:
            field_state = STATE.BLACK

        board = self._engine.get_board()
        if (board[field1[0]][field1[1]] != field_state):
            return False

        # Teraz należy sprawdzić, czy z danego pola
        # da się wykonać ruch tam gdzie chcemy.
        if (field2 not in self._engine.moves(*field1)):
            return False

        return True

    def _parse_move(self, move_str):
        """! Zamienia zapis ruchu na krotkę pól.

        Ta funkcja zakłada poprawność zapisu ruchu.

        @param move_str Zapis ruchu.

        @return Krotka pól.
        """

        y1 = ord(move_str[0]) - ord('a')
        if (y1 < 0):
            y1 += ord('a') - ord('A')

        x1 = ord(move_str[1]) - ord('a')
        if (x1 < 0):
            x1 += ord('a') - ord('A')

        y2 = ord(move_str[3]) - ord('a')
        if (y2 < 0):
            y2 += ord('a') - ord('A')

        x2 = ord(move_str[4]) - ord('a')
        if (x2 < 0):
            x2 += ord('a') - ord('A')

        return ((y1, x1), (y2, x2))

    def _apply_move(self, field1, field2):
        """! Wykonuje ruch.

        @param field1 Pole z którego chcemy się ruszyć.
        @param field2 Pole na które chcemy się ruszyć.
        """

        on_field1 = self._engine.read_field(*field1)
        self._engine.set_field(*field1, STATE.EMPTY)
        self._engine.set_field(*field2, on_field1)

        if (self._engine.moving_player == PLAYER.WHITE):
            # Jeżeli teraz ruszał się biały, to
            # teraz jest kolej na czarnego.
            self._engine.moving_player = PLAYER.BLACK
        else:
            # Jeżeli w danym ruchu ruszył się czarny,
            # przechodzimy do następnego ruchu.
            self._engine.moving_player = PLAYER.WHITE
            self._engine.move += 1

    def move(self, move_str):
        """! Funkcja wykonująca ruch.

        @param move_str Zapis ruchu.

        @return Czy udało się wykonać ruch.
        """

        if (not self._validate_move_str(move_str)):
            return False

        field1, field2 = self._parse_move(move_str)

        if (not self._validate_move(field1, field2)):
            return False

        self._apply_move(field1, field2)
        return True

    def in_camp(self, y, x):
        """! Sprawdza w jakim obozie znajduje się pole.

        @param y Współrzędna Y pola.
        @param x Współrzędna X pola.

        @return W jakim obozie znajduje się pole.
        """

        # Sprawdzamy, czy jest w obozie Czarnego.
        if (x in range(0, 5) and
                y in range(0, [5, 5, 4, 3, 2][x])):
            return CAMP.BLACK

        # Sprawdzamy, czy jest w obozie Białego.
        if (x in range(11, 16) and
                15-y in range(0, [5, 5, 4, 3, 2][15-x])):
            return CAMP.WHITE

        return None

    def get_winner(self):
        """! Sprawdza, czy jest koniec gry.

        Zwraca zwycięzcę w typie wyliczeniowym
        PLAYER.

        @return Zwycięzca.
        """

        board = self._engine.get_board()

        # Gra kończy się gdy w obozie
        # są wszystkie pola zajęte i
        # jest tam co najmniej jeden
        # kamień przeciwnika.
        all_full = True
        enemy_in = False

        # Sprawdzamy obóz Czarnego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                if (board[i][j] == STATE.EMPTY):
                    all_full = False

                if (board[i][j] == STATE.WHITE):
                    enemy_in = True

        if (all_full and enemy_in):
            return PLAYER.WHITE

        all_full = True
        enemy_in = False

        # Sprawdzamy obóz Białego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                if (board[15 - i][15 - j] == STATE.EMPTY):
                    all_full = False

                if (board[15 - i][15 - j] == STATE.BLACK):
                    enemy_in = True

        if (all_full and enemy_in):
            return PLAYER.BLACK

        return None

    def dump_game_state(self):
        """! Zapisuje stan gry w słowniku.

        @return Engine state.
        """

        return self._engine.dump_state()
