#!/usr/bin/python3

# Powłoka pozwalająca na ręczne wywoływanie
# metod klasy Game, która jest w pliku halma.py.
#
# Nie jest on istotną częścią projektu, dołączam
# go dlatego, że może on być tylko być na plus,
# a nie stracę za niego punktów za projekt.
#
# Autor: Antoni Przybylik

import readline
import sys
import cmd2
from tabulate import tabulate
from ast import literal_eval

import halma
from halma import state


class HaSh(cmd2.Cmd):
    # Komendy, których nie chcemy.
    delattr(cmd2.Cmd, 'do_quit')

    # Konfiguracja powłowki.
    intro = 'HAlmaSHell (hash) 1.0.0\n\n' + \
            'Type "help" or "?" to get\n' + \
            'list of supported commands.\n'

    prompt = '\033[36m>>>\033[0m '

    # Wewnętrzne struktuty.
    history_file = '.hash_history'
    games = dict()
    selected_game = None

    def __init__(self):
        super().__init__(persistent_history_file=self.history_file)

    def do_pass(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Does nothing.

        \033[31;1mUsage schemes:\033[0m

        pass
        """

        if (arg_str != ''):
            print('Error: Too many arguments.')
            return

        pass

    def do_new(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Creates new game.

        \033[31;1mUsage schemes:\033[0m

        new <game name>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) > 1):
            print('Error: Too many arguments.')
            return

        if (self.games.get(argv[0], None) is not None):
            print('Error: Name already taken.')
            return

        self.games[argv[0]] = halma.game()

    def do_destroy(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Destroys game.

        \033[31;1mUsage schemes:\033[0m

        destroy <game name>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) > 1):
            print('Error: Too many arguments.')
            return

        if (self.games.get(argv[0], None) is None):
            print('Error: No such game.')
            return

        if (self.games[argv[0]] is self.selected_game):
            self.selected_game = None

        self.games.pop(argv[0])

    def do_select(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Selects game by name.

        \033[31;1mUsage schemes:\033[0m

        select <game name>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) > 1):
            print('Error: Too many arguments.')
            return

        if (self.games.get(argv[0], None) is None):
            print('Error: No such game.')
            return

        self.selected_game = self.games[argv[0]]

    def do_setup(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Sets up selected game in requested mode.

        \033[31;1mUsage schemes:\033[0m

        setup <mode>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) > 1):
            print('Error: Too many arguments.')
            return

        game = self.selected_game

        if (game is None):
            print('Error: No game selected.')
            return

        if (argv[0] not in game.supported_modes):
            print('Error: No such game mode.')
            return

        game.setup(argv[0])

    def do_moves(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Prints possible moves from given position
        in selected game.

        \033[31;1mUsage schemes:\033[0m

        moves <x> <y>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) < 2):
            print('Error: Too few arguments.')
            return

        if (len(argv) > 2):
            print('Error: Too many arguments.')
            return

        game = self.selected_game

        if (game is None):
            print('Error: No game selected.')
            return

        x = int(argv[0])
        y = int(argv[1])

        print(game.moves(x, y))

    def do_list(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Lists games.

        \033[31;1mUsage schemes:\033[0m

        list
        """

        if (arg_str != ''):
            print('Error: Too many arguments.')
            return

        table = []
        for key in self.games.keys():
            game = self.games[key]
            mode = game.mode if game.mode is not None else 'custom'

            pref_str = ''
            suf_str = ''
            if (game is self.selected_game):
                pref_str = '\033[36;1m'
                suf_str = '\033[0m'

            table.append([pref_str + key + suf_str,
                          pref_str + mode + suf_str])

        print(tabulate(table,
                       headers=['GAME', 'MODE'],
                       tablefmt="simple_grid"))

    def do_print(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Prints game board. As an option
        it is possible to highlight
        some fields.

        \033[31;1mUsage schemes:\033[0m

        print [fields to highlight]
        """

        if (arg_str is not None and arg_str != ''):
            to_highlight = literal_eval(arg_str)
            if (type(to_highlight) is not list):
                print('Error: Print accepts list of'
                      'locations as the only argument.')
        else:
            to_highlight = []

        game = self.selected_game

        if (game is None):
            print('Error: No game selected.')
            return

        board = game.get_board()

        for i in range(0, 16):
            for j in range(0, 16):
                if ((i, j) in to_highlight):
                    print('\033[31mH\033[0m', end=' ')
                    continue

                if (board[i][j] == state.EMPTY):
                    print('\033[33m1\033[0m', end=' ')
                elif (board[i][j] == state.WHITE):
                    print('\033[36m2\033[0m', end=' ')
                elif (board[i][j] == state.BLACK):
                    print('\033[32m3\033[0m', end=' ')
                else:
                    raise TypeError('Invalid type for field.')

            print('')

    def do_set_field(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Sets field in some state.

        \033[31;1mUsage schemes:\033[0m

        set <x> <y> <state>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) < 3):
            print('Error: Too few arguments.')
            return

        if (len(argv) > 3):
            print('Error: Too many arguments.')
            return

        game = self.selected_game

        if (game is None):
            print('Error: No game selected.')
            return

        x = int(argv[0])
        y = int(argv[1])

        if (argv[2] == 'EMPTY'):
            game.set_field(x, y, state.EMPTY)
        elif (argv[2] == 'WHITE'):
            game.set_field(x, y, state.WHITE)
        elif (argv[2] == 'BLACK'):
            game.set_field(x, y, state.BLACK)
        else:
            raise ValueError('Not a valid value for field.')

    def do_read_field(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Displays state of requested field.

        \033[31;1mUsage schemes:\033[0m

        read <x> <y>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) < 2):
            print('Error: Too few arguments.')
            return

        if (len(argv) > 2):
            print('Error: Too many arguments.')
            return

        game = self.selected_game

        if (game is None):
            print('Error: No game selected.')
            return

        x = int(argv[0])
        y = int(argv[1])

        value = game.read_field(x, y)
        if (value == state.EMPTY):
            print('EMPTY')
        elif (value == state.WHITE):
            print('WHITE')
        elif (value == state.BLACK):
            print('BLACK')
        else:
            raise ValueError('Corrupted data.')

    def do_exit(self, argv):
        """
        \033[31;1mDescription:\033[0m

        Exits the shell.

        \033[31;1mUsage schemes:\033[0m

        exit
        """

        return True


if __name__ == '__main__':
    HaSh().cmdloop()
