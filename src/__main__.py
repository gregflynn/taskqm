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

    BOARD_NAMES = ['pending', 'started', 'done']
    BOARDS = {
        'pending': Board('pending', '+PENDING -ACTIVE'),
        'started': Board('started', '+ACTIVE'),
        'done': Board('done', '+DONE')
    }
    DEFAULT_BOARD = 'started'
    BACKUP_BOARD = 'pending'
    PROJECTS = set(TaskService.get_projects())

    def __init__(self):
        super().__init__()
        self.project = None
        self._quitting = False

        if self.BOARDS[self.DEFAULT_BOARD].count():
            self.board = self.DEFAULT_BOARD
        else:
            self.board = self.BACKUP_BOARD

        self._status = StatusLine(self)
        self.precmd('')
        self.postcmd(False, '')

    def emptyline(self):
        pass

    def do_project(self, arg):
        self.project = arg if arg else None

    def complete_project(self, text, line, begidx, endidx):
        return sorted([
            name for name in self.PROJECTS if name.startswith(text)
        ])

    def do_board(self, arg):
        if arg not in self.BOARDS:
            print(f'Unknown board specified: {arg}')
            arg = self.DEFAULT_BOARD
        self.board = arg

    def complete_board(self, text, line, begidx, endidx):
        return sorted([
            name for name in self.BOARD_NAMES if name.startswith(text)
        ])

    def do_exit(self, arg):
        return True

    def default(self, arg):
        if arg == 'EOF':
            self._quitting = True
            return True

    def run(self, prompt):
        prompt += self.get_filters()
        run(['task', *prompt.split(' ')])

    def get_filters(self):
        filters = ''

        if self.project:
            filters += f' project:{self.project}'

        return filters

    def precmd(self, line):
        print()
        run(['clear'])
        return line

    @property
    def should_print_board(self):
        return not self._quitting

    def postcmd(self, stop, line):
        if self.should_print_board:
            self.BOARDS[self.board].render(self.get_filters())
            print(self._status.render())
        return stop


if __name__ == '__main__':
    try:
        TaskQM().cmdloop()
    except KeyboardInterrupt:
        pass
