# Bot przesuwający kamienie w
# stronę obozu przeciwnika.
#
# Autor: Antoni Przybylik

from halma.defs import STATE
from halma.defs import PLAYER

from bots.generic import GameBot

from timeout_decorator import timeout
from timeout_decorator import TimeoutError

import copy


class MinimaxBot(GameBot):
    """! Bot używający algorytmu MiniMax. """

    def _dist(self, field1, field2):
        """! Odległość dwóch pól.

        Odległość jest mierzona jako
        liczba ruchów które należy
        wykonać żeby przejść między
        danymi polami ruszając się
        o jedno pole.

        @param field1 Pole na planszy.
        @param field2 Pole na planszy.
        """
        return max(abs(field1[0]-field2[0]),
                   abs(field1[1]-field2[1]))

    def _state_quality(self, board):
        """! Ocenia sytuację na planszy dla gracza białego.

        Sytuacja dla gracza czarnego to -(sytuacja białego).

        @param board Obecny stan planszy.

        @return Ocena sytuacji (im mniejsza tym lepsza).
        """

        # Ocena to będzie suma odległości pionków białych
        # od obozu czarnego - suma odległości pionków czarnych
        # od obozu białego.
        quality = 0

        for i in range(16):
            for j in range(16):
                if (board[i][j] == STATE.WHITE):
                    quality += self._dist((i, j), (0, 0))

                if (board[i][j] == STATE.BLACK):
                    quality -= self._dist((i, j), (15, 15))

        return quality

    def _enemy(self, plr):
        """! Zwraca przeciwnika danego gracza.

        @plr Gracz (biały/czarny)

        @return Przeciwnik.
        """

        if (plr == PLAYER.WHITE):
            return PLAYER.BLACK
        else:
            return PLAYER.WHITE

    def _move_on_board(self, board, field1, field2):
        """! Wykonuje ruch na planszy.

        Przemieszcza pionek z pola 1 na pole 2. Pole 1
        ustawia puste.

        @param field1 Pole 1.
        @param field2 Pole 2.
        """

        board[field2[0]][field2[1]] = board[field1[0]][field1[1]]
        board[field1[0]][field1[1]] = STATE.EMPTY

    def _reverse_move_on_board(self, board, field1, field2):
        """! Wykonuje ruch na planszy.

        Przemieszcza pionek z pola 2 na pole 1. Pole 2
        ustawia puste.

        @param field1 Pole 1.
        @param field2 Pole 2.
        """

        board[field1[0]][field1[1]] = board[field2[0]][field2[1]]
        board[field2[0]][field2[1]] = STATE.EMPTY

    def _minimax(self, board, plr, depth):
        """! Algorytm MiniMax.

        Zwraca ruch tż. zakładając, że
        do depth ruchów w przód przeciwnik
        będzie ruszał się optymalnie, sytuacja
        mierzona przez funkcję _state_quality
        będzie najlepsza.

        Na wszystkich głębokościach rekurencji
        interesuje nas tylko jakość, ale zwracamy
        też wybrany ruch żeby móc odzyskać wynik.
        Wynikiem jest ruch jaki wybraliśmy na
        najwyższym poziomie.

        @param board Plansza do gry.
        @param plr Gracz (biały/czarny)
        @param depth Głębokość rekursji.

        @return Krotka (Wybrany ruch, Jakość stanu po depth ruchach)
        """

        if (depth == 0):
            # Doszliśmy do ostatniego poziomu
            # rekurencji.
            quality = self._state_quality(board)

            if (plr == PLAYER.WHITE):
                return (None, quality)
            else:
                return (None, -quality)

        my_positions = []
        moves_to_consider = []

        for i in range(0, 16):
            for j in range(0, 16):
                field = board[i][j]

                if ((field == STATE.BLACK and
                     plr == PLAYER.BLACK) or
                    (field == STATE.WHITE and
                     plr == PLAYER.WHITE)):
                    my_positions.append((i, j))

        for pos_from in my_positions:
            for pos_to in self._engine.moves(pos_from[0], pos_from[1]):
                moves_to_consider.append((pos_from, pos_to))

        rated_moves = []

        for move in moves_to_consider:
            self._move_on_board(board, *move)
            # Do listy rated_moves dodajemy krotkę:
            # (Ruch, jakość tego ruchu)
            rated_moves.append((move,
                                self._minimax(board,
                                              self._enemy(plr),
                                              depth - 1)[1]))
            self._reverse_move_on_board(board, *move)

        # Uwaga! best_move to krotka (move, quality) !
        best_move = rated_moves[0]
        for rated_move in rated_moves:
            if (rated_move[1] < best_move[1]):
                best_move = rated_move

        return best_move

    def make_move(self):
        """! Wykonuje ruch. """

        board = self._engine.get_board()
        moving_player = self._engine.moving_player

        # W początkowej sytuacji mamy 30 ruchów
        # do wykonania i możemy przejrzeć dużo w
        # przód. W pesymistycznej sytuacji mamy
        # 1000 ruchów do wykonania i możemy przejrzeć
        # co najwyżej dwa.
        @timeout(5)
        def get_move(board, moving_player, depth):
            board_copy = copy.deepcopy(board)
            c_move, c_quality = self._minimax(board_copy, moving_player, depth)
            return c_move

        timed_out = False
        depth = 1
        move = None
        while (not timed_out):
            try:
                computed_move = get_move(board, moving_player, depth)
            except TimeoutError:
                timed_out = True
            else:
                move = computed_move

            depth += 1

        self._apply_move(*move)
