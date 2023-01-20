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

        @param field1 Pole na planszy.
        @param field2 Pole na planszy.
        """
        return max(abs(field1[0]-field2[0]),
                   abs(field1[1]-field2[1]))

    def _dist_to_camp(self, field, camp):
        """! Mierzy odległość do obozu.

        @param field Pole na planszy.
        @param camp Obóz do którego mierzymy odległość.
        """
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

    def _lin_dist_to_corner(self, field, camp):
        """! Mierzy odległość od rogu we wskazanym obozie.

        Odległość jest mierzona w taki sposób, że pola
        stykające się rogiem są od siebie odległe o dwa.

        @param field Pole.
        @param camp Obóz w którym leży róg planszy.
        """
        if (camp == CAMP.WHITE):
            return (15 - field[0]) + (15 - field[1])

        if (camp == CAMP.BLACK):
            return field[0] + field[1]

    def _lin_dist_to_border(self, field, camp):
        """! Mierzy odległość od brzegu przy wskazanym obozie.

        @param field Pole.
        @param camp Obóz przy którym leży brzeg planszy.
        """
        if (camp == CAMP.WHITE):
            return (15 - field[1])

        if (camp == CAMP.BLACK):
            return field[1]

    def _move_quality(self, field1, field2):
        """! Ocenia ruch.

        @param field1 Pole z którego się ruszamy.
        @param field2 Pole na które się ruszamy.
        """
        moving_player = self._engine.moving_player

        if (moving_player == PLAYER.WHITE):
            enemy_camp = CAMP.BLACK
        else:
            enemy_camp = CAMP.WHITE

        quality = 0

        # Jeśli kamień już jest w obozie przeciwnika
        # nie chcemy go ruszać.
        if (self._in_camp(*field1) == enemy_camp):
            quality += -1000

        # Jeśli pionek jest poza obozem, a
        # po ruchu wejdzie do obozu, ruch
        # jest lepszy od wszystkich, w których
        # pionek nie wchodzi do obozu.
        if (self._in_camp(*field1) is None and
                self._in_camp(*field2) == enemy_camp):
            quality += 1000

        quality += (self._dist_to_camp(field1, enemy_camp) -
                    self._dist_to_camp(field2, enemy_camp)) * 10

        # Bot zacinał się przy tylko pierwszym warunku,
        # istnieją sytuacje, że niezależnie od ruchu
        # odległość kamieni od obozu przeciwnika pozostaje
        # taka sama. W takim przypadku należy przesunąć
        # pionek w stronę rogu w obozie przeciwnika.
        quality += (self._lin_dist_to_corner(field1, enemy_camp) -
                    self._lin_dist_to_corner(field2, enemy_camp)) * 5

        # Jeżeli nadal się zacinamy, należy przesunąć
        # pionek w stronę obozu pionowo.
        quality += (self._lin_dist_to_border(field1, enemy_camp) -
                    self._lin_dist_to_border(field2, enemy_camp))

        return quality

    def make_move(self):
        """! Wykonuje ruch. """

        board = self._engine.get_board()
        moving_player = self._engine.moving_player

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
            for pos_to in self._engine.moves(pos_from[0], pos_from[1]):
                moves_to_consider.append((pos_from, pos_to))

        moves_to_consider.sort(reverse=True,
                               key=lambda m: self._move_quality(*m))
        self._apply_move(*moves_to_consider[0])
