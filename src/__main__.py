from cmd import Cmd
from subprocess import run

from .painter import Color, Painter
from .board import Board
from .settings import Settings
from .task_service import TaskService


class TaskQM(Cmd):
    intro = 'Task Quartermaster'
    prompt = Painter.color(Color.BLUE, Settings.PROMPT + ' ')

    BOARDS = {
        'pending': Board('pending', '+PENDING'),
        'started': Board('started', '+STARTED'),
        'done': Board('done', '+DONE')
    }
    DEFAULT_BOARD = 'started'
    PROJECTS = set(TaskService.get_projects())

    def __init__(self):
        super().__init__()
        self.project = None
        self.board = self.DEFAULT_BOARD

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
        boards = self.BOARDS.keys()
        return sorted([name for name in boards if name.startswith(text)])

    def do_exit(self, arg):
        return True

    def default(self, arg):
        if arg == 'EOF':
            return True

    def run(self, prompt):
        prompt += self.get_filters()
        run(['task', *prompt.split(' ')])

    def get_filters(self):
        filters = ''

        if self.project:
            filters += f' project:{self.project}'

        return filters

    def render_status_line(self):
        line = '\n'

        line += Painter.color(Color.GREEN, f'{self.board}')

        if self.project:
            line += Painter.color(Color.PURPLE, f' project:{self.project}')

        print(line)

    def precmd(self, line):
        print()
        return line

    @property
    def should_print_board(self):
        return True

    def postcmd(self, stop, line):
        if self.should_print_board:
            self.BOARDS[self.board].render(self.get_filters())
        self.render_status_line()
        return stop


if __name__ == '__main__':
    try:
        TaskQM().cmdloop()
    except KeyboardInterrupt:
        pass
