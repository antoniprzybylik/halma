# Klasa bazowa reprezentująca gracza.
# Zarówno bota, jak i człowieka.
#
# Po tej klasie może dziedziczyć bot,
# może też gracz-człowiek.
#
# Np. w przypadku gracza człowieka będzie
# zaimplementowana funkcja pytania o ruch
# dialog boxem.
#
# Autor: Antoni Przybylik

class Player:
    """! Klasa reprezentująca gracza. """

    def __init__(self, plr, engine):
        """! Konstruktor klasy player. """
        self._player = plr
        self._engine = engine

    def make_move(self):
        """! Wykonuje ruch.

        @return Wykonany ruch.
        """
        pass
