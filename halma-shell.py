#!/usr/bin/python3

# Powłoka pozwalająca na ręczne wywoływanie
# metod klasy Engine, która jest w pliku halma/engine.py.
#
# Nie jest to istotna cześć projektu.
# Dołączam ją licząc na to, że nie
# przyczyni się do obniżenia oceny
# projektu, a może ją tylko podwyższyć.
# Projekt jest kompletny także bez tego
# pliku.
#
# Autor: Antoni Przybylik

import cmd2
from tabulate import tabulate
from ast import literal_eval

from halma.engine import Engine
from halma.defs import STATE


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
    engines = dict()
    selected_engine = None

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

        Creates new game engine.

        \033[31;1mUsage schemes:\033[0m

        new <engine name>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) > 1):
            print('Error: Too many arguments.')
            return

        if (self.engines.get(argv[0], None) is not None):
            print('Error: Name already taken.')
            return

        self.engines[argv[0]] = Engine()

    def do_destroy(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Destroys game engine.

        \033[31;1mUsage schemes:\033[0m

        destroy <engine name>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) > 1):
            print('Error: Too many arguments.')
            return

        if (self.engines.get(argv[0], None) is None):
            print('Error: No such engine.')
            return

        if (self.engines[argv[0]] is self.selected_engines):
            self.selected_engines = None

        self.engines.pop(argv[0])

    def do_select(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Selects engines by name.

        \033[31;1mUsage schemes:\033[0m

        select <engines name>
        """

        if (arg_str is None or arg_str == ''):
            print('Error: Too few arguments.')
            return

        argv = arg_str.split(' ')

        if (len(argv) > 1):
            print('Error: Too many arguments.')
            return

        if (self.engines.get(argv[0], None) is None):
            print('Error: No such engine.')
            return

        self.selected_engine = self.engines[argv[0]]

    def do_setup(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Sets up game in selected engine in requested mode.

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

        engine = self.selected_engine

        if (engine is None):
            print('Error: No engine selected.')
            return

        if (argv[0] not in engine.supported_modes):
            print('Error: No such game mode.')
            return

        engine.setup(argv[0])

    def do_moves(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Prints possible moves from given position
        in selected game engine.

        \033[31;1mUsage schemes:\033[0m

        moves <y> <x>
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

        engine = self.selected_engine

        if (engine is None):
            print('Error: No engine selected.')
            return

        y = int(argv[0])
        x = int(argv[1])

        print(engine.moves(y, x))

    def do_list(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Lists engines.

        \033[31;1mUsage schemes:\033[0m

        list
        """

        if (arg_str != ''):
            print('Error: Too many arguments.')
            return

        table = []
        for key in self.engines.keys():
            engine = self.engines[key]
            mode = engine.mode if engine.mode is not None else 'custom'

            pref_str = ''
            suf_str = ''
            if (engine is self.selected_engine):
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

        engine = self.selected_engine

        if (engine is None):
            print('Error: No engine selected.')
            return

        board = engine.get_board()

        for i in range(0, 16):
            for j in range(0, 16):
                if ((i, j) in to_highlight):
                    print('\033[31mH\033[0m', end=' ')
                    continue

                if (board[i][j] == STATE.EMPTY):
                    print('\033[33m1\033[0m', end=' ')
                elif (board[i][j] == STATE.WHITE):
                    print('\033[36m2\033[0m', end=' ')
                elif (board[i][j] == STATE.BLACk):
                    print('\033[32m3\033[0m', end=' ')
                else:
                    raise TypeError('Invalid type for field.')

            print('')

    def do_set_field(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Sets field in some state.

        \033[31;1mUsage schemes:\033[0m

        set <y> <x> <state>
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

        engine = self.selected_engine

        if (engine is None):
            print('Error: No engine selected.')
            return

        y = int(argv[0])
        x = int(argv[1])

        if (argv[2] == 'EMPTY'):
            engine.set_field(y, x, STATE.EMPTY)
        elif (argv[2] == 'WHITE'):
            engine.set_field(y, x, STATE.WHITE)
        elif (argv[2] == 'BLACK'):
            engine.set_field(y, x, STATE.BLACk)
        else:
            raise ValueError('Not a valid value for field.')

    def do_read_field(self, arg_str):
        """
        \033[31;1mDescription:\033[0m

        Displays state of requested field.

        \033[31;1mUsage schemes:\033[0m

        read <y> <x>
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

        engine = self.selected_engine

        if (engine is None):
            print('Error: No engine selected.')
            return

        y = int(argv[0])
        x = int(argv[1])

        value = engine.read_field(y, x)
        if (value == STATE.EMPTY):
            print('EMPTY')
        elif (value == STATE.WHITE):
            print('WHITE')
        elif (value == STATE.BLACk):
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
