# Bot przesuwający kamienie w
# stronę obozu przeciwnika.
#
# Autor: Antoni Przybylik

from halma.defs import STATE
from halma.defs import PLAYER
from halma.defs import CAMP

from bots.generic import GameBot


class ForwardBot(GameBot):
    """! Bot przesuwający kamienie w stronę obozu przeciwnika. """

    def _dist(self, field1, field2):
        """! Odległość dwóch pól.

        Odległość jest mierzona jako
        liczba ruchów które należy
        wykonać żeby przejść między
        danymi polami.
        """
        return max(abs(field1[0]-field2[0]),
                   abs(field1[1]-field2[1]))

    def _dist_to_camp(self, field, camp):
        """! Mierzy odległość do obozu. """
        if (camp == CAMP.WHITE):
            return min(self._dist(field, (1, 4)),
                       self._dist(field, (2, 3)),
                       self._dist(field, (3, 2)),
                       self._dist(field, (4, 1)))

        if (camp == CAMP.BLACK):
            return min(self._dist(field, (14, 11)),
                       self._dist(field, (13, 12)),
                       self._dist(field, (12, 13)),
                       self._dist(field, (11, 14)))

    def _move_quality(self, field1, field2):
        """! Ocenia ruch. """
        moving_player = self._game.moving_player

        if (moving_player == PLAYER.WHITE):
            enemy_camp = CAMP.BLACK
        else:
            enemy_camp = CAMP.WHITE

        return self._dist_to_camp(field1, enemy_camp) - \
               self._dist_to_camp(field2, enemy_camp)  # noqa: E127

    def make_move(self):
        """! Wykonuje ruch. """

        board = self._game.get_board()
        moving_player = self._game.moving_player

        my_positions = []
        moves_to_consider = []

        for i in range(0, 16):
            for j in range(0, 16):
                field = board[i][j]

                if ((field == STATE.BLACK and
                     moving_player == PLAYER.BLACK) or
                    (field == STATE.WHITE and
                     moving_player == PLAYER.WHITE)):
                    my_positions.append((i, j))

        for pos_from in my_positions:
            for pos_to in self._game.moves(pos_from[0], pos_from[1]):
                moves_to_consider.append((pos_from, pos_to))

        moves_to_consider.sort(reverse=True,
                               key=lambda m: self._move_quality(*m))
        self._apply_move(*moves_to_consider[0])
