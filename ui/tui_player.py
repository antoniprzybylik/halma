from halma.player import Player


class TuiPlayer(Player):
    """! Gracz przez interfejs TUI """

    def __init__(self, plr, engine, game_iface, ui):
        """! Konstruktor klasy TuiPlayer.

        @param plr Gracz (czarny/biały)
        @param engine Referencja na obiekt Engine
        @param game_iface Referencja na obiekt GameInterface
        """
        self._player = plr
        self._engine = engine
        self._game_iface = game_iface
        self._ui = ui

    def make_move(self):
        """! Wykonuje ruch.

        @return Czy udało się wykonać ruch.
        """
        move_str = self._ui.dialog('Enter your move:', 7, 30)

        while True:
            # Sprawdzamy, czy użytkownik nie
            # zamknął dialog boxa klawiszem escape.
            if (move_str is None):
                return False

            move_str = move_str.rstrip()

            # Próbujemy wykonać ruch.
            if (self._game_iface.move(move_str)):
                return True

            # Dopóki nie udaje się wykonać ruchu wprowadzonego
            # przez użytkownika: Wczytujemy ruch jeszcze raz.
            move_str = self._ui.dialog('Invalid!\n Enter your move:',
                                       8, 30)
