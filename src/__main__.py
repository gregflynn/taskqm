from cmd import Cmd
from subprocess import run

from .painter import Color, Painter
from .board import Board
from .settings import Settings
from .task_service import TaskService
from .status import StatusLine


class TaskQM(Cmd):
    intro = ''
    prompt = Painter.color(Color.BLUE, Settings.PROMPT + ' ')
    doc_header = Painter.color(Color.BLUE, 'Commands: [help command]')
    ruler = ''

    BOARD_NAMES = ['pend', 'start', 'done']
    BOARDS = {
        'pend': Board('pend', '+PENDING -ACTIVE'),
        'start': Board('start', '+ACTIVE'),
        'done': Board('done', '+DONE')
    }
    DEFAULT_BOARD = 'start'
    BACKUP_BOARD = 'pend'
    PROJECTS = set(TaskService.get_projects())
    DEFAULT_ORDER = 'score-'

    # commands that don't alter the board, so we don't clear and reprint it
    NON_BOARD_COMMANDS = {'h', 'help'}

    def __init__(self):
        super().__init__()
        self.project = None
        self.order = self.DEFAULT_ORDER

        if self.BOARDS[self.DEFAULT_BOARD].count():
            self.board = self.DEFAULT_BOARD
        else:
            self.board = self.BACKUP_BOARD

        self._status = StatusLine(self)
        self.precmd('')
        self.postcmd(False, '')

    #
    # Project
    #
    def do_project(self, arg):
        """select the project to filter on
        """
        self.project = arg if arg else None

    def complete_project(self, text, line, begidx, endidx):
        return sorted([
            name for name in self.PROJECTS if name.startswith(text)
        ])

    #
    # Ordering
    #
    def do_order(self, arg):
        """set the board task ordering
        """
        self.order = arg or self.DEFAULT_ORDER

    def complete_order(self, text, line, begidx, endidx):
        matches = []

        for c in Settings.COLUMNS:
            col = c.get('display_name') or c.get('name')
            if not col:
                continue
            if col.startswith(text):
                matches.append(col)

        return matches

    #
    # Board
    #
    def do_board(self, arg):
        """select the board to view
        """
        if arg not in self.BOARDS:
            print(f'Unknown board specified: {arg}')
            arg = self.DEFAULT_BOARD
        self.board = arg

    def complete_board(self, text, line, begidx, endidx):
        return sorted([
            name for name in self.BOARD_NAMES if name.startswith(text)
        ])

    #
    # Help
    #
    do_h = Cmd.do_help
    complete_h = Cmd.complete_help

    #
    # Task Warrior Delegation
    #
    def run(self, prompt):
        prompt += self.get_filters()
        run(['task', *prompt.split(' ')])

    def get_filters(self):
        filters = ''

        if self.project:
            filters += f' project:{self.project}'

        return filters

    #
    # Helpers
    #
    def should_print_board(self, line):
        return not line or line.split()[0] not in {'h', 'help'}

    #
    # Overrides
    #
    def precmd(self, line):
        if line == 'EOF':
            raise KeyboardInterrupt
        if self.should_print_board(line):
            run(['clear'])
            print(f'{self.prompt}{line}')
        return line

    def postcmd(self, stop, line):
        if self.should_print_board(line):
            self.BOARDS[self.board].render(self.get_filters(), self.order)
            print(self._status.render())
        return stop

    def emptyline(self):
        """no-op so the default behavior of execing last command doesn't happen
        """


if __name__ == '__main__':
    try:
        TaskQM().cmdloop()
    except KeyboardInterrupt:
        pass
